format short G

A = importdata('data12.1.tiger.txt','\t');
v1_data = importdata('v112.1.tiger.txt');
v2_data = importdata('v212.1.tiger.txt'); 

v1 = mean(v1_data);
v2 = mean(v2_data);

cmd_bounds = [10,10,240]; %[min_cmd, cmd_step, max_cmd]
force_risetime = 125;
sz = size(A);
A(:,9) = 1:sz(1);

numMagnets = 12;
A(:,10) = A(:,5)*780/numMagnets;

m = 0.2; d = .088; b0 = .142;
%m=added mass, d=distance of mass to pivot, b=distance of motor to pivot,
%v1=reading with no mass, v2=reading with mass.
A(:,11) = (m*d*9.81)*(A(:,8)-v1)/(v2-v1)/b0;

A(:,2) = A(:,2)*0.1;

%1:cmd 2:current 3:maxPWM 4:temp 5:rawRPM 6:reserved1 7:voltage 8:rawForce
%9:count 10:RPM 11:thrust

data = bitfilter(A);
data = rpmfilter(data,10);

rpmdata = modefilter(data,5,2,cmd_bounds);
f1 = fit(rpmdata(:,1),rpmdata(:,10),'poly3');

forcedata = forcefilter0(data,force_risetime,cmd_bounds);
f2 = fit(forcedata(:,1),forcedata(:,11),'poly3');

f3 = fit(forcedata(:,1),forcedata(:,2),'poly3');


A0 = importdata('2827.txt','\t');
v1_data0 = importdata('v1.2827.txt');
v2_data0 = importdata('v2.2827.txt'); 

v10 = mean(v1_data0);
v20 = mean(v2_data0);

cmd_bounds0 = [10,10,240]; %[min_cmd, cmd_step, max_cmd]
force_risetime0 = 125;
sz0 = size(A0);
A0(:,9) = 1:sz0(1);

numMagnets0 = 12;
A0(:,10) = A0(:,5)*780/numMagnets0;

m = 0.2; d = .088; b = .158;
%m=added mass, d=distance of mass to pivot, b=distance of motor to pivot,
%v1=reading with no mass, v2=reading with mass.
A0(:,11) = (m*d*9.81)*(A0(:,8)-v10)/(v20-v10)/b;

A0(:,2) = A0(:,2)*0.1;

%1:cmd 2:current 3:maxPWM 4:temp 5:rawRPM 6:reserved1 7:voltage 8:rawForce
%9:count 10:RPM 11:thrust

data0 = bitfilter(A0);
data0 = rpmfilter(data0,10);

rpmdata0 = modefilter(data0,5,2,cmd_bounds0);
f10 = fit(rpmdata0(:,1),rpmdata0(:,10),'poly3')
figure(1);
plot(f10,'k',rpmdata0(:,1),rpmdata0(:,10),'.','k');hold on;
plot(f1,rpmdata(:,1),rpmdata(:,10))
legend('2827 Motor','','2827 Motor','Tiger Motor','Tiger Motor','Location','Southeast')
xlabel('Command')
ylabel('RPM')
grid on

forcedata0 = forcefilter(data0,force_risetime0,cmd_bounds0);
f20 = fit(forcedata0(:,1),forcedata0(:,11),'poly3')
figure(2);
plot(f20,'k',forcedata0(:,1),forcedata0(:,11),'.','k');hold on;
plot(f2,forcedata(:,1),forcedata(:,11))
legend('2827 Motor','','2827 Motor','Tiger Motor','Tiger Motor','Location','Southeast')
xlabel('Command')
ylabel('Force (N)')
grid on

f30 = fit(forcedata0(:,1),forcedata0(:,2),'poly3')
figure(3);
plot(f30,'k',forcedata0(:,1),forcedata0(:,2),'.','k'); hold on;
plot(f3,forcedata(:,1),forcedata(:,2))
legend('2827 Motor','','2827 Motor','Tiger Motor','Tiger Motor','Location','Southeast')
xlabel('Command')
ylabel('Current (A)')
grid on

f4 = fit(forcedata(:,11),forcedata(:,4),'poly3')
f40 = fit(forcedata0(:,11),forcedata0(:,4),'poly3')
figure(4);
plot(f40,'k',forcedata0(:,11),forcedata0(:,4),'.','k');hold on;
plot(f4,forcedata(:,11),forcedata(:,4))
legend('2827 Motor','','2827 Motor','Tiger Motor','Tiger Motor','Location','Southeast')
xlabel('Force')
ylabel('Temp')
grid on

f5 = fit(forcedata(:,11),forcedata(:,2),'poly3')
f50 = fit(forcedata0(:,11),forcedata0(:,2),'poly3')
figure(5);
plot(f50,'k',forcedata0(:,11),forcedata0(:,2),'.','k');hold on;
plot(f5,forcedata(:,11),forcedata(:,2))
legend('2827 Motor','','2827 Motor','Tiger Motor','Tiger Motor','Location','Southeast')
xlabel('Force')
ylabel('Current')
grid on

efficiency = forcedata(:,11)./forcedata(:,2);
efficiency0 = forcedata0(:,11)./forcedata0(:,2);

f6 = fit(forcedata(:,11),forcedata(:,2),'poly3')
f60 = fit(forcedata0(:,11),forcedata0(:,2),'poly3')
figure(5);
plot(f50,'k',forcedata0(:,11),forcedata0(:,2),'.','k');hold on;
plot(f5,forcedata(:,11),forcedata(:,2))
legend('2827 Motor','','2827 Motor','Tiger Motor','Tiger Motor','Location','Southeast')
xlabel('Force')
ylabel('Current')
grid on