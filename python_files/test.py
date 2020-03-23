import scipy.io.wavfile
import pydub
import numpy as np
import matplotlib.pyplot as plt
import time
import librosa
from scipy.fftpack import fft

audData, rate = librosa.core.load("floor_eleven.wav", sr=None)
sampData, rate = librosa.core.load("eleven_8k_short.wav", sr=None)

audtime = np.arange(0, len(audData), 1)
samptime = np.arange(0, len(sampData), 1)

frequency_samp = np.linspace(0.0, 512, int(len(samptime)/2))
frequency_aud = np.linspace(0.0, 512, int(len(audtime)/2))

freq_data_samp = fft(sampData)
freq_data_aud = fft(audData)

X_sample = 2/len(samptime)*np.abs(freq_data_samp[0:np.int(len(samptime)/2)])
X_audio = 2/len(audtime)*np.abs(freq_data_aud[0:np.int(len(audtime)/2)])

print(X_sample)

plt.figure(0)
plt.subplot(211)
plt.plot(samptime, sampData, linewidth=0.05, alpha=0.9, label='beep_sample')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(212)
plt.plot(frequency_samp, X_sample, linewidth=0.1, alpha=1, label='FFT')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.legend()

plt.show()

cross_cor = np.zeros([len(audtime)])
buffer = np.zeros(len(X_sample))
Xjw_buf = np.zeros(len(X_sample))
delay = np.zeros([len(audtime)])
DFT = np.zeros([len(audtime)])
hits = np.zeros([len(audtime)])

print(len(audtime))
print(len(X_sample))
timer = time.time()
i = 0
while i <= len(audtime)-1:
    sumi=  0
    #cross_cor_t[i] = audData[i]*sampData[0]
    #Xjw_buf = 2/len(buffer)*np.abs(fft(buffer)[0:len(buffer)/2])
    for k in range(0, len(X_sample)-1):
        sumi += buffer[N-k]*np.exp(-2j*np.pi*counter/len(Xjw_buf)*(N-k))#np.abs(buffer[N-k]*np.exp(-2j*np.pi/len(Xjw_buf)*(N-k)*counter))
        cross_cor[i] +=  Xjw_buf[N-k] * X_sample[N-k]
        #cross_cor_t[N-k] += buffer[N-k] * sampData[N-k]
        buffer[N-k] = buffer[(N-1)-k]
        Xjw_buf[N-k] = Xjw_buf[(N-1)-k]
    buffer[0] = audData[i]
    Xjw_buf[0] = sumi
    #print(Xjw_buf[len(X_sample)-1])
    if counter >= len(X_sample):
        counter = 0
        """
        plt.figure(0)
        plt.subplot(211)
        plt.plot(np.arange(0, len(X_sample)), 2/len(X_sample)*np.abs(fft(buffer)), linewidth = 0.8, alpha = 0.9)
        plt.subplot(212)
        plt.plot(np.arange(0, len(X_sample)), 2/len(X_sample)*np.abs(Xjw_buf), linewidth = 0.8, alpha = 0.9)
        plt.show()
        """
    if abs(cross_cor[i]) > 2.75:
        #print("we got a hit!!")
        hits[i] = 1
    counter += 1
    i += 1

delay = time.time() - timer

print(hits)
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
