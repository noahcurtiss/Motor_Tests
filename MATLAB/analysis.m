function forcedata = analysis(file_name)
format short G

A = importdata(strcat(file_name, '.txt'),'\t');
v1_data = importdata(strcat(file_name, 'v1.txt'));
v2_data = importdata(strcat(file_name, 'v2.txt')); 

v1 = mean(v1_data);
v2 = mean(v2_data);

cmd_bounds = [10,10,250]; %[min_cmd, cmd_step, max_cmd]
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
A(:,7) = A(:,7)*.1;

%1:cmd 2:current 3:maxPWM 4:temp 5:rawRPM 6:reserved1 7:voltage 8:rawForce
%9:count 10:RPM 11:thrust

data = bitfilter(A);
data = rpmfilter(data,10);

forcedata = forcefilter(data,force_risetime,cmd_bounds);

end

