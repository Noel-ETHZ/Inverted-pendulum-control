import sympy as sp

# Define symbols (parameters and variables from state/input)
M, m, g, l, theta, theta_dot, F = sp.symbols('M m g l theta theta_dot F')

# Trig terms for convenience
cos_theta = sp.cos(theta)
sin_theta = sp.sin(theta)

# Unknowns to solve for
x_ddot, theta_ddot = sp.symbols('x_ddot theta_ddot')

eq1 = g * theta - 3/2 * l *(2/(m*l)*F-(2*x_ddot*(M/(m*l)+1/l)))-x_ddot
eq2 = 2/(m*l)*F - 2 *(M/(m*l)+ 1/l)*(g*theta - 3/2*l*theta_dot)-theta_ddot

#solve the equations for x_ddot and theta_ddot
solution = sp.solve([eq1, eq2], [x_ddot, theta_ddot])

print("x_ddot =")
sp.pprint(solution[x_ddot])
print("\ntheta_ddot =")
sp.pprint(solution[theta_ddot])