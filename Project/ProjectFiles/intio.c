/*************************************************************************************
			       DEPARTMENT OF ELECTRICAL AND ELECTRONIC ENGINEERING
					   		     IMPERIAL COLLEGE LONDON 

 				      EE 3.19: Real Time Digital Signal Processing
					       Dr Paul Mitcheson and Daniel Harvey

				        		  LAB 3: Interrupt I/O

 				            ********* I N T I O. C **********

  Demonstrates inputing and outputing data from the DSK's audio port using interrupts. 

 *************************************************************************************
 				Updated for use on 6713 DSK by Danny Harvey: May-Aug 2006
				Updated for CCS V4 Sept 10
 ************************************************************************************/
/*
 *	You should modify the code so that interrupts are used to service the 
 *  audio port.
 */
/**************************** Pre-processor statements ******************************/

#include <stdlib.h>
//  Included so program can make use of DSP/BIOS configuration tool.  
#include "dsp_bios_cfg.h"

/* The file dsk6713.h must be included in every program that uses the BSL.  This 
   example also includes dsk6713_aic23.h because it uses the 
   AIC23 codec module (audio interface). */
#include "dsk6713.h"
#include "dsk6713_aic23.h"
//#include "coef.txt"
// math library (trig functions)
#include <math.h>

// Some functions to help with writing/reading the audio ports when using interrupts.
#include <helper_functions_ISR.h>
//double b[] = {0.05882352941, 0.05882352941};
//double a[] = {1, -0.88235294117};

#include "dsk6713_led.h"
#include "fftsample_coef.txt"

#include <complex.h>

double cross_cor[2] = {0};
int length;
int i;
int counter;
double derivative[2] = {0};

double PI = 3.14159265;

typedef double complex cplx;

int buffer[2082] = {0};
double FFT[2082] = {0};
double sum_re;
double sum_im;


/******************************* Global declarations ********************************/

/* Audio port configuration settings: these values set registers in the AIC23 audio 
   interface to configure it. See TI doc SLWS106D 3-3 to 3-10 for more info. */
DSK6713_AIC23_Config Config = { \
			 /**********************************************************************/
			 /*   REGISTER	            FUNCTION			      SETTINGS         */ 
			 /**********************************************************************/\
    0x0017,  /* 0 LEFTINVOL  Left line input channel volume  0dB                   */\
    0x0017,  /* 1 RIGHTINVOL Right line input channel volume 0dB                   */\
    0x01f9,  /* 2 LEFTHPVOL  Left channel headphone volume   0dB                   */\
    0x01f9,  /* 3 RIGHTHPVOL Right channel headphone volume  0dB                   */\
    0x0011,  /* 4 ANAPATH    Analog audio path control       DAC on, Mic boost 20dB*/\
    0x0000,  /* 5 DIGPATH    Digital audio path control      All Filters off       */\
    0x0000,  /* 6 DPOWERDOWN Power down control              All Hardware on       */\
    0x0043,  /* 7 DIGIF      Digital audio interface format  16 bit                */\
    0x008d,  /* 8 SAMPLERATE Sample rate control             8 KHZ                 */\
    0x0001   /* 9 DIGACT     Digital interface activation    On                    */\
			 /**********************************************************************/
};


// Codec handle:- a variable used to identify audio interface  
DSK6713_AIC23_CodecHandle H_Codec;

 /******************************* Function prototypes ********************************/
void init_hardware(void);     
void init_HWI(void);
void InteruptFunc(void);
void dir2filter(void);
void dir2Tfilter(void);
void signal_detection(void);
void cross_correlation(void);
/********************************** Main routine ************************************/
 void main(){
     DSK6713_LED_on(3);
    // initialize board and the audio port
    init_hardware();
    /* initialize hardware interrupts */
    init_HWI();
    /* loop indefinitely, waiting for interrupts */
    DSK6713_LED_off(3);

    length = sizeof(coef)/sizeof(coef[0])-1;
    while(1)
    {};
}
/********************************** init_hardware() **********************************/  
void init_hardware()
{
    // Initialize the board support library, must be called first 
    DSK6713_init();
    
    // Start the AIC23 codec using the settings defined above in config 
    H_Codec = DSK6713_AIC23_openCodec(0, &Config);

	/* Function below sets the number of bits in word used by MSBSP (serial port) for 
	receives from AIC23 (audio port). We are using a 32 bit packet containing two 
	16 bit numbers hence 32BIT is set for  receive */
	MCBSP_FSETS(RCR1, RWDLEN1, 32BIT);	

	/* Configures interrupt to activate on each consecutive available 32 bits 
	from Audio port hence an interrupt is generated for each L & R sample pair */	
	MCBSP_FSETS(SPCR1, RINTM, FRM);

	/* These commands do the same thing as above but applied to data transfers to  
	the audio port */
	MCBSP_FSETS(XCR1, XWDLEN1, 32BIT);	
	MCBSP_FSETS(SPCR1, XINTM, FRM);	
	//Initialise the LED's
	DSK6713_LED_init();
}

/********************************** init_HWI() **************************************/  
void init_HWI(void)
{
	IRQ_globalDisable();			// Globally disables interrupts
	IRQ_nmiEnable();				// Enables the NMI interrupt (used by the debugger)
	IRQ_map(IRQ_EVT_RINT1,4);		// Maps an event to a physical interrupt
	IRQ_enable(IRQ_EVT_RINT1);		// Enables the event
	//IRQ_enable(IRQ_EVT_XINT1);
	IRQ_globalEnable();				// Globally enables interrupts

} 

/******************** WRITE YOUR INTERRUPT SERVICE ROUTINE HERE***********************/  
void InteruptFunc(void)
{
    signal_detection();
    mono_write_16Bit(cross_cor[0]);   //Write output to codec
}

void signal_detection(void)
{
    buffer[0] = mono_read_16Bit();
    sum_re = 0;
    sum_im = 0;
    for (i=2082; i>0;i--){
        sum_re +=  buffer[i] * cos(i*counter*2*PI/2082);
        sum_im -= buffer[i] * sin(i*counter*PI*2/2082);
        cross_cor[0] += FFT[i] * coef[i];
        buffer[i] = buffer[i-1];
        FFT[i] = FFT[i-1];
    }
    FFT[0]= sum_re*sum_re + sum_im*sum_im;
    derivative[0] = cross_cor[1]-cross_cor[0];
    if(derivative[0]*derivative[1] < 0){
        DSK6713_LED_on(3);
    }
    else{
        DSK6713_LED_off(3);
    }
    if(counter >= length)
    {
        counter = 0;
    }
    counter += 1;
    buffer[1] = buffer[0];
    cross_cor[1] = cross_cor[0];
    cross_cor[0] = 0;
    derivative[1] = derivative[0];
}

void cross_correlation(void)
{
    buffer[0] = mono_read_16Bit();
    for(i=2082; i>0; i--)
    {
        cross_cor[0] += buffer[i] * coef[i] ;
        buffer[i] = buffer[i-1];
    }
    buffer[1] = buffer[0];
    cross_cor[1] = cross_cor[0];
    cross_cor[0] = 0;
}
