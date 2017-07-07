a =1;
for i = 10:10:210
    cmdmatrix = cmdfilter(data,i);
    figure(a);
    scatter(cmdmatrix(:,9),cmdmatrix(:,11))
    a= a+1;
end