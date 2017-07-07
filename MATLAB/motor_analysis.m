format short G

A = importdata('data.tiger.txt','\t');
v1_data = importdata('v1.tiger.txt');
v2_data = importdata('v2.tiger.txt'); 

v1 = mean(v1_data);
v2 = mean(v2_data);

cmd_bounds = [10,10,210]; %[min_cmd, cmd_step, max_cmd]
force_risetime = 125;
sz = size(A);
A(:,9) = 1:sz(1);

numMagnets = 12;
A(:,10) = A(:,5)*780/numMagnets;

m = 0.2; d = .088; b = .142;
%m=added mass, d=distance of mass to pivot, b=distance of motor to pivot,
%v1=reading with no mass, v2=reading with mass.
A(:,11) = (m*d*9.81)*(A(:,8)-v1)/(v2-v1)/b;

A(:,2) = A(:,2)*0.1;

%1:cmd 2:current 3:maxPWM 4:temp 5:rawRPM 6:reserved1 7:voltage 8:rawForce
%9:count 10:RPM 11:thrust

data = bitfilter(A);
data = rpmfilter(data,10);

rpmdata = modefilter(data,5,2,cmd_bounds);
f1 = fit(rpmdata(:,1),rpmdata(:,10),'poly3')
figure(1);
plot(f1,rpmdata(:,1),rpmdata(:,10))
xlabel('Command')
ylabel('RPM')
grid on

forcedata = forcefilter(data,force_risetime,cmd_bounds);
f2 = fit(forcedata(:,1),forcedata(:,11),'poly3')
figure(2);
plot(f2,forcedata(:,1),forcedata(:,11))
xlabel('Command')
ylabel('Force (N)')
grid on

f3 = fit(forcedata(:,1),forcedata(:,2),'poly3')
figure(3);
plot(f3,forcedata(:,1),forcedata(:,2))
xlabel('Command')
ylabel('Current (A)')
grid on