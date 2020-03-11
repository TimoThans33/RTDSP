import scipy.io.wavfile
import pydub
import numpy as np
import matplotlib.pyplot as plt
from terminalplot import plot
import time
from scipy.fftpack import fft


rate,audData=scipy.io.wavfile.read("journey_no_noise_8k.wav")
rate, sampData = scipy.io.wavfile.read("beep_8k(1).wav")

audtime = np.arange(0, float(audData.shape[0]), 1)
samptime = np.arange(0, float(sampData.shape[0]), 1)

frequency_samp = np.linspace(0.0, 512, int(len(samptime)))
frequency_aud = np.linspace(0.0, 512, int(len(audtime)))

freq_data_samp = fft(sampData)
freq_data_aud = fft(audData)

X_sample = 2/len(samptime)*np.abs(freq_data_samp[0:np.int(len(samptime))])
X_audio = 2/len(audtime)*np.abs(freq_data_aud[0:np.int(len(audtime))])

cross_cor = np.zeros([len(audtime)])
buffer = np.zeros(20)
delay = np.zeros([len(audtime)])
DFT = np.zeros([len(audtime)])

hits = []

print(len(audtime))
print(len(samptime))
for i in range(0,len(audtime)-1):
    timer = time.time()
    cross_cor[i] = X_audio[i]*X_sample[0]
    for k in range(len(buffer)-1, 1):
        cross_cor[i] +=  Xjw_buf[k]* X_sample[k]
        buffer[k] = buffer[k-1]
    buffer[1] = audData[i]
    Xjw_buf = 2/len(buffer)*np.abs(fft(buffer)[0:len(buffer)])
    if abs(cross_cor[i] > 0.0019):
        print("we got a hit!!")
        hits.append(i)
    delay[i] = time.time() - timer

print(hits)



plt.figure(0)
plt.subplot(211)

plt.plot(audtime, X_audio, linewidth=0.02, alpha=0.9)
"""
for i in range(0, len(hits)-1):
    plt.plot(hits[i]+samptime, sampData, linewidth=0.02, alpha=0.9, color='red')
    """
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.plot(audtime, cross_cor, linewidth=0.5, alpha=0.9)
"""
for i in range(0, len(hits)-1):
    plt.plot(hits[i]+samptime, sampData, linewidth=0.01, alpha=0.9, color='red')
"""
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.figure(1)
plt.subplot(211)
plt.plot(frequency_samp, X_sample, linewidth=0.1, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.plot(audtime, delay, linewidth=0.1, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('delay')
plt.ylim(0, 5*10**-5)
plt.show()
