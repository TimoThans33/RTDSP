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

float a1[] = {1 ,-7.80973974, 2.68412482e+01,-5.30198282e+01, 6.58319005e+01,-5.26124756e+01 ,2.64303907e+01 ,-7.63111434e+00 ,9.69621051e-01};
float b1[] = {9.85496564e-02 ,-7.72311598e-01 ,2.66384542 ,-5.28134630 ,6.58252588,-5.28134630 ,2.66384542 ,-7.72311598e-01 ,9.85496564e-02};
//double b2[] = 9.75649439e-02 ,-3.42867427e-01 ,4.91100538e-01 ,-3.42867427e-01 ,9.75649439e-02 ,
//double b1[] = 00000001 ,-3.62273828e+00 ,5.06388779e+00 ,-3.23461026e+00 ,7.98416468e-01 ,>>

float yout;
float sample;
int order = 9;
float w[9];
float v[9];
int i;
int k;
float h;

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
double bandpass(void);
/********************************** Main routine ************************************/
 void main(){
    // initialize board and the audio port
    init_hardware();
    /* initialize hardware interrupts */
    init_HWI();
    /* loop indefinitely, waiting for interrupts */
    //order = sizeof(a1)/sizeof(a1[0])-1;
    //w = (float *) calloc(order+1, sizeof(float));
    //v = (float *) calloc(order+1, sizeof(float));
    for (i=0; i <order; i++){
        v[i] = 0;
        w[i] = 0;
    }
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
    v[0] = 1;
    h = bandpass();
    mono_write_16Bit((Int16) h);   //Write output to codec
}

double bandpass(void)
{
    yout = b1[0]*v[0];
    for (k=order; k>0;k--){
        yout += v[k]*b1[k] - w[k]*a1[k];
        w[k] = w[k-1];
        v[k] = v[k-1];
    }
    v[1] = v[0];
    w[1] = yout;
    return yout;
    /*
    yout = 0;
    for (i = 8; i>0; i--){
        v[0] -= a1[i]*v[i]; //implements left
        yout += b1[i]*v[i]; //implements right
        v[i] = v[i-1];
    }
    yout += b1[0]*v[0];
    return yout;
    */
}
