i = 1;
for volt = 10.8:0.2:12.6
    file_name = compose("tiger%.1f",volt);
    v1_data = importdata(strcat(file_name, 'v1.txt'));
    v2_data = importdata(strcat(file_name, 'v2.txt')); 

    v1 = mean(v1_data);
    v2 = mean(v2_data);
    
    matrix(i,:) = [volt, v1, v2];
    i = i+1;
end
matrix