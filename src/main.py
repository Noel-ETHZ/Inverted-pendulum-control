import numpy as np
import control as ct
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from dynamics import get_nonlinear_dynamics
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#parameters definition

M = 1 #mass of cart
m = 0.1 #mass of pendulum
l = 0.5 #length of pendulum
g = 9.81 #acceleration due to gravity

#state space representation
A = np.array([[0, 1, 0, 0],
              [0, 0, 7*g*m/(7*M+4*m), 0],
              [0, 0, 0, 1],
              [0, 0, -6*g*(m+M)/(l*(7*M+4*m)), 0]])
B = np.array([[0],  
              [7/(7*M+4*m)],
              [0],
              [-6/(l*(7*M+4*m))]])

C = np.array([0, 0, 1, 0])  # Output matrix (1x4)
D = np.array([0])          # Direct transmission matrix (1x1)


# LQR setup
Q = np.diag([1, 1, 10, 1])  # State cost matrix (penalizes angle position more)
R = np.array([[0.1]])  # Input cost matrix

# Compute the LQR gain
K, S, E = ct.lqr(A, B, Q, R)
K = np.asarray(K)

def closed_loop_dynamics(state, t, K, ref_state, params):
    # Compute control input
    error = state - ref_state
    F = - (K @ error)[0]
    # Now use F in dynamics
    return get_nonlinear_dynamics(t, state, F, params)


# Simulation parameters
initial_state = np.array([0.0, 0.0, 0.1, 0.0])  # Small theta offset
t_span = np.linspace(0, 10, 1000)  # 10 sec, many points
ref_state = np.array([0.0, 0.0, 0.0, 0.0])
params = {'M': 1.0, 'm': 0.1, 'l': 0.5, 'g': 9.81}

states = odeint(closed_loop_dynamics, initial_state, t_span, args=(K, ref_state, params))





# --------------------------------------------------# Plotting setup

# Create plots
fig = plt.figure(figsize=(15, 10))

# Animation subplot
ax_anim = plt.subplot(2, 2, (1, 2))
ax_anim.set_xlim(-2, 2)
ax_anim.set_ylim(-1, 1)
ax_anim.set_aspect('equal')
ax_anim.grid(True)
ax_anim.set_title('Inverted Pendulum Animation')
ax_anim.set_xlabel('Position (m)')
ax_anim.set_ylabel('Height (m)')

# Cart position plot
ax1 = plt.subplot(2, 2, 3)
ax1.plot(t_span, states[:, 0])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Cart Position x (m)')
ax1.set_title('Cart Position over Time')
ax1.grid(True)

# Pendulum angle plot
ax2 = plt.subplot(2, 2, 4)
ax2.plot(t_span, states[:, 2])
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Pendulum Angle θ (rad)')
ax2.set_title('Pendulum Angle over Time')
ax2.grid(True)

plt.tight_layout()

# --------------------------------------------------
# Animation setup
cart_width = 0.3
cart_height = 0.15
wheel_radius = 0.05
pendulum_length = params['l']
floor_level = -cart_height/2 - wheel_radius

# Draw floor
floor_line, = ax_anim.plot([-2, 2], [floor_level, floor_level], 'k-', linewidth=4, alpha=0.8)

# Initialize animation objects
cart = plt.Rectangle((0, 0), cart_width, cart_height, fill=True, color='blue', alpha=0.7)
ax_anim.add_patch(cart)

# Add wheels
left_wheel = plt.Circle((0, 0), wheel_radius, color='black', fill=True)
right_wheel = plt.Circle((0, 0), wheel_radius, color='black', fill=True)
ax_anim.add_patch(left_wheel)
ax_anim.add_patch(right_wheel)

# Add wheel spokes for rotation visualization
left_spoke1, = ax_anim.plot([], [], 'white', linewidth=2)
left_spoke2, = ax_anim.plot([], [], 'white', linewidth=2)
right_spoke1, = ax_anim.plot([], [], 'white', linewidth=2)
right_spoke2, = ax_anim.plot([], [], 'white', linewidth=2)

pendulum_line, = ax_anim.plot([], [], 'r-', linewidth=8, solid_capstyle='round')
# Removed pendulum_bob - no particle at the end

# Time indicator lines for the plots
time_line1, = ax1.plot([], [], 'r--', alpha=0.7)
time_line2, = ax2.plot([], [], 'r--', alpha=0.7)

def animate(frame):
    # Get current state
    x = states[frame, 0]
    theta = states[frame, 2]
    current_time = t_span[frame]
    
    # Update cart position
    cart.set_x(x - cart_width/2)
    cart.set_y(-cart_height/2)
    
    # Update wheel positions
    wheel_y = floor_level + wheel_radius
    left_wheel_x = x - cart_width/4
    right_wheel_x = x + cart_width/4
    
    left_wheel.center = (left_wheel_x, wheel_y)
    right_wheel.center = (right_wheel_x, wheel_y)
    
    # Calculate wheel rotation based on cart displacement
    wheel_rotation = x / wheel_radius  # Simple rotation calculation
    
    # Update wheel spokes (create rotating cross pattern)
    spoke_length = wheel_radius * 0.7
    cos_rot = np.cos(wheel_rotation)
    sin_rot = np.sin(wheel_rotation)
    
    # Left wheel spokes
    left_spoke1.set_data([left_wheel_x - spoke_length * cos_rot, left_wheel_x + spoke_length * cos_rot],
                        [wheel_y - spoke_length * sin_rot, wheel_y + spoke_length * sin_rot])
    left_spoke2.set_data([left_wheel_x - spoke_length * sin_rot, left_wheel_x + spoke_length * sin_rot],
                        [wheel_y + spoke_length * cos_rot, wheel_y - spoke_length * cos_rot])
    
    # Right wheel spokes
    right_spoke1.set_data([right_wheel_x - spoke_length * cos_rot, right_wheel_x + spoke_length * cos_rot],
                         [wheel_y - spoke_length * sin_rot, wheel_y + spoke_length * sin_rot])
    right_spoke2.set_data([right_wheel_x - spoke_length * sin_rot, right_wheel_x + spoke_length * sin_rot],
                         [wheel_y + spoke_length * cos_rot, wheel_y - spoke_length * cos_rot])
    
    # Calculate pendulum position (from top center of cart)
    cart_top_y = cart_height/2  # Top of the cart
    pendulum_base_x = x
    pendulum_base_y = cart_top_y
    pendulum_tip_x = x + pendulum_length * np.sin(theta)
    pendulum_tip_y = cart_top_y + pendulum_length * np.cos(theta)
    
    # Update pendulum (attached to top of cart)
    pendulum_line.set_data([pendulum_base_x, pendulum_tip_x], [pendulum_base_y, pendulum_tip_y])
    
    # Update time indicators on plots
    y_range1 = ax1.get_ylim()
    y_range2 = ax2.get_ylim()
    time_line1.set_data([current_time, current_time], y_range1)
    time_line2.set_data([current_time, current_time], y_range2)
    
    return (cart, left_wheel, right_wheel, left_spoke1, left_spoke2, 
            right_spoke1, right_spoke2, pendulum_line, 
            time_line1, time_line2)

# Create animation (every 3rd frame for slower, smoother playback)
anim = FuncAnimation(fig, animate, frames=range(0, len(t_span), 6), 
                    interval=50, blit=True, repeat=True)

plt.show()

# Optional: Save the animation in the plots directory (set to False to skip saving)
SAVE_ANIMATION = True  # Change to False if you don't want to save

if SAVE_ANIMATION:
    print("Saving animation to GIF file...")
    
    import os
    plots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    from matplotlib.animation import PillowWriter
    writer = PillowWriter(fps=20)
    
    anim.save(os.path.join(plots_dir, 'pendulum_animation.gif'), writer=writer)
    
    print("Animation saved successfully!")
else:
    print("Animation not saved (SAVE_ANIMATION = False)")