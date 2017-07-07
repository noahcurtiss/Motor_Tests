function B = voltfilter( A,volt )
B = zeros(1,11);
sz = size(A);
a = 1;
for i = 1:sz(1)
    if A(i,7) == volt
        B(a,:) = A(i,:);
        a = a+1;
    end
end
end

