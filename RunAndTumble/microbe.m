function [  ] = microbe(n,a,b)
%Simulates "run and tumble" method of unicellular movement.
%   Plots n microbes with linear speed a and angular speed b moving into
%   higher compound densities. Uses an approximated gradient ascent system
%   found in biology.

set(gcf,'Units','normalized','OuterPosition',[0.25,0.25,0.75,0.75]);

[X,Y]=meshgrid(0:1:100,0:1:100);
Z = compounds(X,Y);

x = zeros(1000,n);
y = zeros(1000,n);
density = zeros(1000,n);
orient = randn(1,n);

x(1,:) = 100*rand(1,n);
y(1,:) = 100*rand(1,n);
density(1,:) = compounds(x(1,:),y(1,:));
for i = 2:1000
    density(i,:) = compounds(x(i-1,:),y(i-1,:));
    for j = 1:n
        if density(i,j) >= density(i-1,j)
            x(i,j) = mod(x(i-1,j)+a*cos(orient(j)),100);
            y(i,j) = mod(y(i-1,j)+a*sin(orient(j)),100);
        else
            orient(j) = orient(j) + normrnd(0,b);
            x(i,j) = x(i-1,j);
            y(i,j) = y(i-1,j);
        end
    end
    imagesc(Z)
    axis([0 100 0 100])
    hold on
    for j = 1:n
        plot(x(i,j),y(i,j),'or','MarkerSize',5,'MarkerFaceColor','r')
    end
    pause(.001)
    hold off
end

end

