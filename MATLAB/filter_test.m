no_filter = importdata('nofilter.txt',',');
LPF5 = importdata('LPF5.txt',',');
LPF10 = importdata('LPF10.txt',',');
LPF20 = importdata('LPF20.txt',',');
LPF42 = importdata('LPF42.txt',',');
LPF98 = importdata('LPF98.txt',',');
LPF188 = importdata('LPF188.txt',',');

figure(1);
plot(no_filter(:,1),no_filter(:,5))

figure(2);
plot(LPF5(:,1),LPF5(:,5))

figure(3);
plot(LPF10(:,1),LPF10(:,5))

figure(4);
plot(LPF20(:,1),LPF20(:,5))

figure(5);
plot(LPF42(:,1),LPF42(:,5))

figure(6);
plot(LPF98(:,1),LPF98(:,5))

figure(7);
plot(LPF188(:,1),LPF188(:,5))