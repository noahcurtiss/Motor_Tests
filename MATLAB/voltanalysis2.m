format short G

total = zeros(1,11);

for v = 10.8:0.2:12.6
    file_name = compose("tiger%.1f",v);
    data  = analysis(file_name);
    total = [total;data];
end

total = total(2:end,:);

C = zeros(1,3);
i = 1;
for cmd = 10:10:250
    D = cmdfilter(total,cmd);
    for volt = 10.3:0.1:13.0
        E = voltfilter(D,volt);
        if E(1,11) ~= 0
            C(i,1) = volt;
            C(i,2) = cmd;
            C(i,3) = mean(E(:,11));
            i = i+1;
        end
    end
end

% [xq,yq] = meshgrid(10.3:.1:13.0, 10:10:250);
% zq = griddata(C(:,1),C(:,2),C(:,3),xq,yq);
% mesh(xq,yq,zq);
% hold on
% plot3(C(:,1),C(:,2),C(:,3),'o')
% xlim([10 13])
% ylim([0 260])


[xq,yq] = meshgrid(10.3:.1:13.0, 0:.05:8);
zq = griddata(C(:,1),C(:,3),C(:,2),xq,yq);
mesh(xq,yq,zq);
hold on
plot3(C(:,1),C(:,3),C(:,2),'o')
xlim([10 13])
ylim([0 8])