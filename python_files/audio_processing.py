import scipy.io.wavfile
import pydub
import numpy as np
import matplotlib.pyplot as plt
from terminalplot import plot
import time
import librosa
from scipy.fftpack import fft

"""
rate,audData = scipy.io.wavfile.read("3beeps.wav")
rate, sampData = scipy.io.wavfile.read("beep_8k_short.wav")

audtime = np.linspace(0, 1.59, int(audData.shape[0]))
samptime = np.arange(0, float(sampData.shape[0]), 1)

plt.figure(0)
plt.subplot(211)
plt.plot(audtime, audData, linewidth=0.02, alpha=0.9)

plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.figure(1)
plt.subplot(211)
plt.plot(samptime, sampData, linewidth=0.1, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
"""

audData, rate = librosa.core.load("3beeps.wav", sr = None)
sampData, rate = librosa.core.load("beep_8k_short.wav", sr = None)

audtime = np.arange(0, len(audData), 1)
samptime = np.arange(0, len(sampData), 1)

"""
plt.figure(0)
plt.subplot(212)
plt.plot(audtime, audData, linewidth=0.02, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.figure(1)
plt.subplot(212)
plt.plot(samptime, sampData, linewidth=0.5, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('delay')
plt.show()
"""

cross_cor = np.zeros([len(audtime)])
buffer = np.zeros([len(samptime)])
delay = np.zeros([len(audtime)])
hits = []
N = len(samptime)-1

print(len(audData))
print(len(sampData))

for i in range(0,len(audtime)-1):
    timer = time.time()
    cross_cor[i] = audData[i]*sampData[0]
    for k in range(0, len(samptime)-1):
        cross_cor[i] += buffer[k] * sampData[k]
        buffer[N-k] = buffer[(N-1)-k]
    buffer[0] = audData[i]
    if abs(cross_cor[i] > 0.3):
        print("we got a hit!!")
        print("cross correlation =", cross_cor[i])
        hits.append(i)
    delay[i] = time.time() - timer

print(hits)




plt.figure(0)
plt.plot(audtime, audData, linewidth=0.05, alpha=0.08, label='input signal')
for i in range(0, len(hits)-1):
    plt.bar(hits[i], height = 0.4, width = 50, bottom=-0.2, alpha=0.1,
     color='red', label='hits')

plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.xticks()
plt.yticks()

plt.figure(1)
plt.plot(audtime, cross_cor, linewidth=0.02, alpha=0.9, label='beep sample')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.xticks()
plt.yticks()
