fc = 159
fs = 8000
[b, a] = butter(1, fc/(fs/2));
b1 = [0.0588235 0.0588235]
a1 = [1 -0.8823529]
figure(1)
freqz(b1,a1)
[h, f] = freqz(b1,a1,5000, fs)
figure(2)
plot(f, db(h))
y = db(h)
x = f
