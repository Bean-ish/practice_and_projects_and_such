
% graph the section
f = @(x) cos(x);
x_values = linspace(0, pi/2, 100);
y_values = f(x_values);
plot(x_values, y_values);


% for k = 1:40
%     h = pi/(2*((2^k)+1));
%     if h < 1e-6
%         break
%     end
%     fprintf('numbers: %f', k);
%     fprintf('h values: %f', h);
% end

% get result from ^ 
% k = 1:20




% (a) composite midpoint
n = 3;
h = (pi/2) / n;  % size
x = linspace(0, pi/2, n+1);
y = f(x);  % evaluate the function at all the equally spaced points
y1 = f(x+h/2);  % evaluate at x+h/2
approximation = h * (y1(1) + sum(y1(2:1:end-1)) + y1(end));

mabser = [];
approximation_new = 0;
a = 0;
for k = 1:20
    n = 2^k + 1; 
    
    x = linspace(0, pi/2, n+1);
    h = (pi/2) / n;
    y = f(x);
    y1 = f(x+h/2);  
    approximation_new = h * (y1(1) + sum(y1(2:1:end-1)) + y1(end));
    
    a = 1-approximation_new;
    mabser = [mabser a];
end

% Display the result
fprintf('Approximation by Composite Midpoint Rule: %.8f\n', approximation_new);
fprintf('Number of subinterval: %f', n);

merror = log(mabser);





% (b) composite trapezoid

n = 3;
h = (pi/2) / n;  % size
x = linspace(0, pi/2, n+1);
y = f(x);
approximation = h * ((1/2)*y(1) + sum(y(2:1:end-1)) + (1/2)*y(end));

tabser = [];
approximation_new = 0;
for k = 1:20
    n = 2^k + 1; 
    
    x = linspace(0, pi/2, n+1);
    h = (pi/2) / n;
    y = f(x);
    approximation_new = h * ((1/2)*y(1) + sum(y(2:1:end-1)) + (1/2)*y(end));
    
    a = 1-approximation_new;
    tabser = [tabser a];

end

% Display the result
fprintf('Approximation by Composite Trapezoid Rule: %.8f\n', approximation_new);
fprintf('Number of subintervals: %f', n);

terror = log(tabser);





% (c) composite simpsons
n = 3;
h = (pi/2) / n;  % size
x = linspace(0, pi/2, n+1);
y = f(x);
% approximation = h * ((1/2)*y(1) + sum(y(2:1:end-1)) + (1/2)*y(end));

sabser = [];
approximation_new = 0;
for k = 1:20
    n = (2^k + 1); 
    
    x = linspace(0, pi/2, n+1);
    h = (pi/2) / n;  % step size
    y = f(x);
    approximation_new = h/3 * (y(1) + 4*sum(y(2:2:end-1)) + 2*sum(y(3:2:end-2)) + y(end));
    
    a = 1-approximation_new;
    sabser = [sabser a];
end

% Display the result
fprintf('Approximation by Composite Simpson''s Rule: %.8f\n', approximation_new);
fprintf('Number of subintervals: %f', n);

serror = log(sabser);





% (d) plotting

% log h
t_log = linspace(1,20,20);
loghf = @(t) log(pi/2*((2.^t)+1));
logh = loghf(t_log);


plot(logh, merror, 'r', logh, terror, 'g-', logh, serror, 'b');
legend('Midpoint', 'Trapezoid', 'Simpson''s');
xlabel('log(h)');
ylabel('log(1-approximation)');
title('abs error against log(h)');

% explanation: Error of midpoint rule is larger than that of trapezoid
% rule, and error of trapezoid rule is larger than that of simpson's
% rule
