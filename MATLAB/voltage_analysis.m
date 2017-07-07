format short G

graph_matrix = zeros(1,3);
total = zeros(1,11);
voltage = [10.8,0.2,12.6]; %min, step, max

for v = voltage(1):voltage(2):voltage(3)
    file_name = compose("tiger%.1f",v);
    data  = analysis(file_name);
    A(:,2) = 10:10:250;
    A(:,1) = v;
    i = 1;
    for cmd = 10:10:250
        B = cmdfilter(data,cmd);
        A(i,3) = mean(B(:,11));
        i = i+1;
    end
    graph_matrix = [graph_matrix;A];
    total = [total;data];
end
graph_matrix = graph_matrix(2:end,:);
total = total(2:end,:);

[xq,yq] = meshgrid(voltage(1):voltage(2):voltage(3), 10:10:250);
zq = griddata(graph_matrix(:,1),graph_matrix(:,2),graph_matrix(:,3),xq,yq);
mesh(xq,yq,zq);
hold on
plot3(graph_matrix(:,1),graph_matrix(:,2),graph_matrix(:,3),'o')
xlim([(voltage(1)-voltage(2)) (voltage(3)-voltage(2))])
ylim([0 260])
