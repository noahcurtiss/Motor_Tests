function maxbit = bitfilter(A)
sz = size(A);
a = 1;
for i = 1:sz(1)
    if A(i,3) == 255
        maxbit(a,:) = A(i,:);
        a = a+1;
    end
end
end

