import sympy as sp
import numpy as np

# Define symbols (parameters and variables from state/input)
M, m, g, l, theta, theta_dot, F = sp.symbols('M m g l theta theta_dot F')

# Trig terms for convenience
cos_theta = sp.cos(theta)
sin_theta = sp.sin(theta)

# Unknowns to solve for
x_dot, x_ddot, theta_dot, theta_ddot = sp.symbols('x_dot x_ddot theta_dot theta_ddot')

eq1 = (M + m) * x_ddot + (1/2) * m * l * theta_ddot * sp.cos(theta) - F
eq2 = (7/12) * m * l**2 * theta_ddot + (1/2) * m * l * x_ddot * sp.cos(theta) + (1/2) * m * g * l * sp.sin(theta)


# Apply small-angle approximations: sin(theta) ≈ theta, cos(theta) ≈ 1
eq1_lin = eq1.subs({sp.sin(theta): theta, sp.cos(theta): 1})
eq2_lin = eq2.subs({sp.sin(theta): theta, sp.cos(theta): 1})

# Solve the linearized system for x_ddot and theta_ddot
linearized_solutions = sp.solve([eq1_lin, eq2_lin], (x_ddot, theta_ddot), simplify=True)
non_linearized_solutions = sp.solve([eq1, eq2], (x_ddot, theta_ddot), simplify=True)


def get_nonlinear_dynamics(t, state, F, params):
    """
    Returns the nonlinear dynamics equations for the inverted pendulum system.
    """
    M, m, l, g = params['M'], params['m'], params['l'], params['g']
    x, x_dot, theta, theta_dot = state

    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    sin_2_theta = np.sin(2 * theta)
    cos_2_theta = np.cos(2 * theta)
        
    # Cart acceleration
    x_ddot = (14.0*F + 3.0*g*m*sin_2_theta)/(14.0*M - 3.0*m*cos_2_theta + 11.0*m)

    # Pendulum angular acceleration
    theta_ddot = 6.0*(F*cos_theta + M*g*sin_theta+ g*m*sin_theta)/(l*(-7.0*M + 3.0*m*cos_theta**2 - 7.0*m))

    return np.array([x_dot, x_ddot, theta_dot, theta_ddot])