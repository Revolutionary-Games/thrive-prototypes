function [ z ] = compounds(x,y)
%Compound density function over a 100x100 grid.
%   Must use element-wise operations (e.g. use .* instead of *). For best
%   results, use a function which wraps around 0:100 by 0:100 without
%   discontinuities, e.g. periodic in x and y directions with period 100 in
%   both.
    z = sin(x.*(pi/100))+sin(y.*(pi/100));
end

