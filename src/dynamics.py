import sympy as sp

# Define symbols (parameters and variables from state/input)
M, m, g, l, theta, theta_dot, F = sp.symbols('M m g l theta theta_dot F')

# Trig terms for convenience
cos_theta = sp.cos(theta)
sin_theta = sp.sin(theta)

# Unknowns to solve for
x_ddot, theta_ddot = sp.symbols('x_ddot theta_ddot')

eq1 = (M + m) * x_ddot + (1/2) * m * l * theta_ddot * sp.cos(theta) - F
eq2 = (7/12) * m * l**2 * theta_ddot + (1/2) * m * l * x_ddot * sp.cos(theta) + (1/2) * m * g * l * sp.sin(theta)

# Apply small-angle approximations: sin(theta) ≈ theta, cos(theta) ≈ 1
eq1_lin = eq1.subs({sp.sin(theta): theta, sp.cos(theta): 1})
eq2_lin = eq2.subs({sp.sin(theta): theta, sp.cos(theta): 1})

# Solve the linearized system for x_ddot and theta_ddot
linearized_solutions = sp.solve([eq1_lin, eq2_lin], (x_ddot, theta_ddot), simplify=True)

print(linearized_solutions)