[y, fs] = audioread('beep_8k_short.wav')
Y = fft(y)
for i = 1:length(y)
    fprintf(' %f,',y(i))
end
fprintf(' \n')
for i = 1:length(y)
    fprintf(' %f,', Y(i))
end
plot(abs(Y))