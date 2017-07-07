function b = cmdfilter(A,cmd)
sz = size(A);
a = 1;
for i = 1:sz(1)
    if A(i,1) == cmd
        b(a,:) = A(i,:);
        a = a+1;
    end
end
end

