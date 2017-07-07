function B = forcefilter0(A,risetime,cmd_bounds)
a = 1;
for i = cmd_bounds(1):cmd_bounds(2):cmd_bounds(3)
    cmd = cmdfilter(A,i);
    sz = size(cmd);
    mincount = min(cmd(:,9));
    if i==30|i==40|i==100
       for j = 1:sz(1)
           if (cmd(j,9)-mincount)>=250
               B(a,:) = cmd(j,:);
               a = a+1;
           end
        end
    else
        for j = 1:sz(1)
            if (cmd(j,9)-mincount)>=risetime
                B(a,:) = cmd(j,:);
                a = a+1;
            end
        end
    end
end
end

