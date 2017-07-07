function B = rpmfilter(A,minrpm)
sz = size(A);
a = 1;
for i = 1:sz(1)
    if A(i,5) >= minrpm
        B(a,:) = A(i,:);
        a = a+1;
    end
end
end

