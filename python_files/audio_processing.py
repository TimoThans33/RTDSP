import scipy.io.wavfile
import pydub
import numpy as np
import matplotlib.pyplot as plt
from terminalplot import plot
import time


rate,audData=scipy.io.wavfile.read("journey_no_noise_8k.wav")
rate, sampData = scipy.io.wavfile.read("beep_8k(1).wav")

audtime = np.arange(0, float(audData.shape[0]), 1)
samptime = np.arange(0, float(sampData.shape[0]), 1)

cross_cor = np.zeros([len(audtime)])
buffer = np.zeros([len(samptime)])
delay = np.zeros([len(audtime)])
hits = []
print(len(audtime))
print(len(samptime))
for i in range(0,len(audtime)-1):
    timer = time.time()
    cross_cor[i] = audData[i]*sampData[0]
    for k in range(len(samptime)-1, 1):
        cross_cor[i] += buffer[k] * sampData[k]
        buffer[k] = buffer[k-1]
    buffer[1] = audData[i]
    if abs(cross_cor[i] > 0.0015):
        print("we got a hit!!")
        hits.append(i)
    delay[i] = time.time() - timer

print(hits)
    
    
    

plt.figure(0)
plt.subplot(211)

plt.plot(audtime, audData, linewidth=0.02, alpha=0.9)
for i in range(0, len(hits)-1):
    plt.plot(hits[i]+samptime, sampData, linewidth=0.02, alpha=0.9, color='red')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.plot(audtime, cross_cor, linewidth=0.02, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.figure(1)
plt.subplot(211)
plt.plot(samptime, sampData, linewidth=0.1, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.plot(audtime, delay, linewidth=0.1, alpha=0.9)
plt.xlabel('Time (s)')
plt.ylabel('delay')
plt.ylim(0, 5*10**-5)
plt.show()
