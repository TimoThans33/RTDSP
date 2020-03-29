import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import time
import librosa
from scipy.fftpack import fft
import multiprocessing

audData, rate = librosa.core.load("../SoundSamples/journey_no_noise_8k.wav", sr = None)
sampData_floor11, rate = librosa.core.load("../SoundSamples/eleven_8k_short.wav", sr = None)
sampData_beep, rate = librosa.core.load("../SoundSamples/beep_8k_short.wav", sr = None)

audtime = np.arange(0, len(audData), 1)
samptime_floor11 = np.arange(0, len(sampData_floor11), 1)
samptime_beep = np.arange(0, len(sampData_beep), 1)

"""
Define here your window sizes
"""
WINDOW_SIZE_FLOOR11 = 100

WINDOW_SIZE_BEEP = 20

"""
Define here your minimum values
"""
MIN_VALUE_FLOOR11 = 2.01

MIN_VALUE_BEEP = 0.1

#cross_cor_floor11 = np.zeros([len(audtime)])
#cross_cor_beep = np.zeros([len(audtime)])

def computer_floor11(cross_cor_floor11, hits_floor11, count_floor11):
    print("starting p1......")
    timer = time.time()
    i = 0
    counter = 0
    pointer = 0
    buffer = np.zeros([len(samptime_floor11)])
    array = np.zeros([len(audtime)])
    array1 = np.zeros([len(audtime)])
    while i <= len(audtime)-1:
        buffer[pointer] = audData[i]
        if counter > WINDOW_SIZE_FLOOR11:
            for k in range(len(buffer)):
                array[i-WINDOW_SIZE_FLOOR11-1:i] += buffer[k]*sampData_floor11[k] 
            counter = 0
            if abs(array[i-5]) > MIN_VALUE_FLOOR11:
                array1[i-WINDOW_SIZE_FLOOR11-1:i] = 1
                if array1[i-WINDOW_SIZE_FLOOR11-1] == 1 and array1[i-WINDOW_SIZE_FLOOR11-2] == 0:
                    count_floor11.value += 1
                #print("hit")
        i += 1
        pointer += 1
        counter += 1
        if pointer >= len(buffer)-1:
            pointer = 0
    cross_cor_floor11[:] = array
    hits_floor11[:] = array1
    print("p1 finished in:",time.time()-timer)

def computer_beep(cross_cor_beep, hits_beep, count_beeps):
    print("starting p2.....")
    timer = time.time()
    g = 0
    counter = 0
    pointer = 0
    buffer = np.zeros([len(samptime_beep)])
    array = np.zeros([len(audtime)])
    array1 = np.zeros([len(audtime)])
    while g <= len(audtime)-1:
        buffer[pointer] = audData[g]
        if counter > WINDOW_SIZE_BEEP:
            for k in range(len(buffer)):
                array[g-WINDOW_SIZE_BEEP-1:g] += buffer[k]*sampData_beep[k]
            counter=0
            if abs(array[g-5]) > MIN_VALUE_BEEP:
                array1[g-WINDOW_SIZE_BEEP-1:g] = 1
                if array1[g-WINDOW_SIZE_BEEP-1] == 1 and array1[g-WINDOW_SIZE_BEEP-2] == 0:
                    count_beeps.value += 1
                #print("hit")
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
        plt.plot(audtime/1000, audData, linewidth=0.5, alpha=0.9, label = 'Journey no noise')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.subplot(312)
        plt.plot(audtime/1000, array1, linewidth=0.8, alpha=0.9, color = 'r')
        plt.xlabel('Time (s)')
        plt.ylabel('Hit beep')

        plt.subplot(313)
        plt.plot(audtime/1000, array2, linewidth=0.8, alpha=0.9)
        plt.xlabel('Time (s)')
        plt.ylabel('Hit floor11')
        plt.show()
          
if __name__ =="__main__":
    cross_cor_floor11 = multiprocessing.Array('f', len(audtime))
    cross_cor_beep = multiprocessing.Array('f', len(audtime))

    hits_floor11 = multiprocessing.Array('f', len(audtime))
    hits_beep = multiprocessing.Array('f', len(audtime))

    count_beeps = multiprocessing.Value('i', 0)
    count_floor11 = multiprocessing.Value('i', 0)
    
    p1 = multiprocessing.Process(target=computer_floor11, args = (cross_cor_floor11, hits_floor11, count_floor11))
    p2 = multiprocessing.Process(target=computer_beep, args = (cross_cor_beep, hits_beep, count_beeps))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    np.save("../.npy/cross_cor_total_floor11.npy", cross_cor_floor11[:])
    np.save("../.npy/cross_cor_total_beep.npy", cross_cor_beep[:])

    #cross_cor_beep = np.load("cross_cor_total_beep.npy")
    #cross_cor_floor11 = np.load("cross_cor_total_floor11.npy")
    
    plot(cross_cor_beep[:], cross_cor_floor11[:])
    plot(hits_beep[:], hits_floor11[:])

    print("beep count : ", count_beeps.value)
    print("floor11 count : ", count_floor11.value)


"""

if __name__ =="__main__":
    thread1 = threading.Thread(target=computer_floor11)
    thread2 = threading.Thread(target=computer_beep)
    thread1.start()
    thread2.start()
    while True:
        if Done1 and Done2 == True:
            plot()
            break
                        
"""
