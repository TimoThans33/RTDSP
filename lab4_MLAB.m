clf;
f = [355 415 1200 1270];
a = [0 1 0];
fs = 8000;
rp = 0.5;
rs = 48;
dev = [10^(-rs/20) (10^(rp/20)-1)/(10^(rp/20)+1)  10^(-rs/20)]; 
[n,fo,ao,w] = firpmord(f,a,dev,fs);
b = firpm(n,fo,ao,w);
disp(n);
[h, f] = freqz(b, 1 ,5000,fs);
plot(f, db(h));


for i = 1:249
    fprintf('%.8d ,', b(i))
end

%save coef.txt x -tabs;
%type('coef.txt');
ax = gca;
ax.YLim = [-70 20];
ax.XLim = [0 10000];