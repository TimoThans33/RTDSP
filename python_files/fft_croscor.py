import scipy.io.wavfile
import pydub
import numpy as np
import matplotlib.pyplot as plt
import time
import librosa
import threading
from scipy.fftpack import fft

"""
Read audio samples and do the FFT
"""
audData, rate = librosa.core.load("3beeps.wav", sr=None)
sampData, rate = librosa.core.load("beep_8k_short.wav", sr=None)

audtime = np.arange(0, len(audData), 1)
samptime = np.arange(0, len(sampData), 1)

frequency_samp = np.linspace(0.0, 512, int(len(samptime)/2))
frequency_aud = np.linspace(0.0, 512, int(len(audtime)/2))

freq_data_samp = fft(sampData)
freq_data_aud = fft(audData)

X_sample = np.zeros([len(samptime)])
X_sample[0:np.int(len(samptime)/2)] = 2/len(samptime)*np.abs(freq_data_samp[0:np.int(len(samptime)/2)])
X_audio = 2/len(audtime)*np.abs(freq_data_aud[0:np.int(len(audtime)/2)])

"""
Define here your window size: this is the refresh rate of the FFT
"""

WINDOW_SIZE = 500

"""
Define here the sensitivity
"""

MIN_VALUE = 0.00039

"""
Plot the beep in the time and frequency domain.
"""
def plotjes():
    plt.figure(0)
    plt.subplot(211)
    plt.plot(samptime, sampData, linewidth=0.2, alpha=1, label='beep_sample')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(212)
    plt.plot(frequency_samp, X_sample[0:np.int(len(samptime)/2)], linewidth=0.8, alpha=0.8, label='FFT')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()

    """
    Plot the long journey in the time domain
    """
    plt.figure(1)
    plt.plot(audtime, audData, linewidth = 0.05, alpha =0.9, label="long_journey")
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.show()

"""
Initialize arrays
"""
cross_cor = np.zeros([len(audtime)])
buffer = np.zeros(len(samptime))
Xjw_buf = np.zeros(len(samptime))#np.zeros(len(X_sample), dtype=np.complex_)
hits = np.zeros([len(audtime)])
N = len(samptime)-1
counter = 0

"""
def FFT():
    global i
    global counter
    global WINDOW_SIZE
    timer = time.time()
    while i <= len(audtime)-1:
        if counter >=WINDOW_SIZE:
            Xjw_buf[0:int(len(buffer)/2)] = 2/len(buffer)*np.abs(fft(buffer)[0:int(len(buffer)/2)])
            counter = 0
        counter += 1
    time
            
def Cross_cor():
    global i
    global MIN_VALUE
    print(len(audtime))
    while i <= len(audtime)-1:
        for k in range(0, len(samptime)-1):
            cross_cor[i] += Xjw_buf[N-k] * X_sample[N-k]
            buffer[N-k] = buffer[(N-1)-k]
        buffer[0] = audData[i]
        if abs(cross_cor[i]) > MIN_VALUE:
            hits[i] = 1
        i += 1

    

initialize threads

thread_FFT = threading.Thread(target = FFT)
thread_CC = threading.Thread(target = Cross_cor)
thread_FFT.start()
thread_CC.start()

"""
print(len(X_sample))
timer = time.time()
i = 0
while i <= len(audtime)-1:
    for k in range(0, len(samptime)-1):
        cross_cor[i] += Xjw_buf[N-k] * X_sample[N-k]
        buffer[N-k] = buffer[(N-1)-k]
    buffer[0] = audData[i]
    if counter >= WINDOW_SIZE:
        Xjw_buf[0:int(len(buffer)/2)] = 2/len(buffer)*np.abs(fft(buffer)[0:int(len(buffer)/2)])
        counter = 0
    if abs(cross_cor[i]) > MIN_VALUE:
        hits[i] = 1
        """
        print(Xjw_buf)
        frequency_samp2 = np.linspace(0.0, 512, int(len(buffer)/2))
        plt.figure(0)
        plt.subplot(311)
        #plt.plot(frequency_samp, fft(buffer))
        plt.plot(frequency_samp, 2/len(X_sample)*np.abs(fft(buffer)), linewidth = 0.8, alpha = 0.9)
        plt.subplot(312)
        plt.plot(frequency_samp, X_sample, linewidth = 0.8, alpha = 0.9)
        plt.subplot(313)
        plt.plot(frequency_samp, Xjw_buf, linewidth = 0.8, alpha = 0.9)
        plt.show()
        """       
    counter += 1
    i += 1

delay = time.time() - timer

print(delay)
plt.figure(0)
plt.plot(audtime, cross_cor, linewidth=0.2, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')


plt.figure(1)
plt.subplot(211)
plt.plot(audtime, audData, linewidth=0.1, alpha=0.9)
plt.xlabel('time (s)')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.plot(audtime, hits, linewidth=0.4, alpha=0.9)
plt.xlabel('time (s)')
plt.show()

