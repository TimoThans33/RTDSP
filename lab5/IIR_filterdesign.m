fs = 8000
n = 1
Wn = 0.125
[b a] = butter(n,Wn)
freqz(b,a,100000, fs)