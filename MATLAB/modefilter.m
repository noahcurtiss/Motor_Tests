function b = modefilter(A,pos,range,cmd_bounds)
a = 1;
for j = cmd_bounds(1):cmd_bounds(2):cmd_bounds(3)
    cmd = cmdfilter(A,j);
    posmode = mode(cmd(:,pos));
    sz = size(cmd);
    for i = 1:sz(1)
        if cmd(i,pos)>=(posmode-range) && cmd(i,pos)<=(posmode+range)
            b(a,:) = cmd(i,:);
            a = a+1;
        end
    end
end
end

