import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import time
import librosa
from scipy.fftpack import fft
import multiprocessing

audData_floor11, rate = librosa.core.load("../SoundSamples/journey_no_noise_8k.wav", sr = None)
audData_beep, rate = librosa.core.load("../SoundSamples/journey_no_noise_8k.wav", sr = None)

sampData_floor11, rate = librosa.core.load("../SoundSamples/eleven_8k_short.wav", sr = None)
sampData_beep, rate = librosa.core.load("../SoundSamples/beep_8k_short.wav", sr = None)

audtime_floor11 = np.arange(0, len(audData_floor11), 1)
audtime_beep = np.arange(0, len(audData_beep), 1)

samptime_floor11 = np.arange(0, len(sampData_floor11), 1)
samptime_beep = np.arange(0, len(sampData_beep), 1)

freq_data_samp_floor11 = fft(sampData_floor11)
freq_data_samp_beep = fft(sampData_beep)

X_sample_floor11 = np.zeros([len(samptime_floor11)])
X_sample_beep = np.zeros([len(samptime_beep)])
X_sample_floor11[0:np.int(len(samptime_floor11)/2)] = 2/len(samptime_floor11)*np.abs(freq_data_samp_floor11[0:np.int(len(samptime_floor11)/2)])
X_sample_beep[0:np.int(len(samptime_beep)/2)] = 2/len(samptime_beep)*np.abs(freq_data_samp_beep[0:np.int(len(samptime_beep)/2)])


"""
Define here your window sizes
"""
WINDOW_SIZE_FLOOR11 = 1200

WINDOW_SIZE_BEEP = 400

"""
Define here your minimum values
"""
MIN_VALUE_FLOOR11 = 0.0112

MIN_VALUE_BEEP = 0.0004

#cross_cor_floor11 = np.zeros([len(audtime)])
#cross_cor_beep = np.zeros([len(audtime)])

def computer_floor11(cross_cor_floor11, hits_floor11):
    print("starting p1......")
    timer = time.time()
    i = 0
    counter = 0
    pointer = 0
    buffer = np.zeros([len(samptime_floor11)])
    Xjw_buf = np.zeros([len(samptime_floor11)])
    array = np.zeros([len(audtime_floor11)])
    array1 = np.zeros([len(audtime_floor11)])
    while i <= len(audtime_beep)-1:
        buffer[pointer] = audData_floor11[i]
        if counter > WINDOW_SIZE_FLOOR11: 
            Xjw_buf[0:int(len(buffer)/2)] = 2/len(buffer)*np.abs(fft(buffer)[0:int(len(buffer)/2)])
            for k in range(len(buffer)):
                array[i-WINDOW_SIZE_FLOOR11-1:i] += Xjw_buf[k]*X_sample_floor11[k] 
            counter = 0
            if abs(array[i-5]) > MIN_VALUE_FLOOR11:
                array1[i-WINDOW_SIZE_FLOOR11-1:i] = 1
        i += 1
        pointer += 1
        counter += 1
        if pointer >= len(buffer)-1:
            pointer = 0
    cross_cor_floor11[:] = array
    hits_floor11[:] = array1
    print("p1 finished in:",time.time()-timer)

def computer_beep(cross_cor_beep, hits_beep):
    print("starting p2.....")
    timer = time.time()
    g = 0
    counter = 0
    pointer = 0
    buffer = np.zeros([len(samptime_beep)])
    Xjw_buf = np.zeros([len(samptime_beep)])
    array = np.zeros([len(audtime_beep)])
    array1 = np.zeros([len(audtime_beep)])
    while g <= len(audtime_beep)-1:
        buffer[pointer] = audData_beep[g]
        if counter > WINDOW_SIZE_BEEP:
            Xjw_buf[0:int(len(buffer)/2)] = 2/len(buffer)*np.abs(fft(buffer)[0:int(len(buffer)/2)])
            for k in range(len(buffer)):
                array[g-WINDOW_SIZE_BEEP-1:g] += Xjw_buf[k]*X_sample_beep[k]
            counter=0
            if abs(array[g-5]) > MIN_VALUE_BEEP:
                array1[g-WINDOW_SIZE_BEEP-1:g] = 1
        g += 1
        pointer += 1                   
        counter += 1
        if pointer >= len(buffer)-1:
            pointer = 0
    cross_cor_beep[:] = array
    hits_beep[:] = array1
    print("p2 finished in:",time.time()-timer)

def plot(array1, array2):
        plt.figure(0)
        plt.subplot(311)
        plt.plot(audtime_beep/1000, audData_beep, linewidth=0.5, alpha=0.9, label = 'Journey no noise')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.subplot(312)
        plt.plot(audtime_beep/1000, array1, linewidth=0.8, alpha=0.9, color = 'r')
        plt.xlabel('Time (s)')
        plt.ylabel('Hit beep')

        plt.subplot(313)
        plt.plot(audtime_floor11/1000, array2, linewidth=0.8, alpha=0.9)
        plt.xlabel('Time (s)')
        plt.ylabel('Hit floor11')
        plt.show()
          
if __name__ =="__main__":
    cross_cor_floor11 = multiprocessing.Array('f', len(audtime_floor11))
    cross_cor_beep = multiprocessing.Array('f', len(audtime_beep))

    hits_floor11 = multiprocessing.Array('f', len(audtime_floor11))
    hits_beep = multiprocessing.Array('f', len(audtime_beep))

    p1 = multiprocessing.Process(target=computer_floor11, args = (cross_cor_floor11, hits_floor11))
    p2 = multiprocessing.Process(target=computer_beep, args = (cross_cor_beep, hits_beep))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    np.save("../.npy/cross_cor_total_fft_floor11.npy", cross_cor_floor11[:])
    np.save("../.npy/cross_cor_total__fft_beep.npy", cross_cor_beep[:])

    #cross_cor_beep = np.load("cross_cor_total_beep.npy")
    #cross_cor_floor11 = np.load("cross_cor_total_floor11.npy")
    
    plot(cross_cor_beep[:], cross_cor_floor11[:])
    plot(hits_beep[:], hits_floor11[:])
