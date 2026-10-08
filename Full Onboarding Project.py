PythonFinalizationError
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

@dataclass
# Class that describes the state of the car, including horizontal and vertical position, horizontal velocity, and time
class State:
    xpos : float
    ypos : float
    xvel : float
    time : float

time_step = 0.3

def step (state:State) -> State:
# Part 1 Variables
    mass = 300 # kg, includes driver
    max_torque = 180 # Newtons * Meters
    gear_ratio = 3 
    radius = 0.216 # Meters

# Part 1 Initialization 
    if state.time <= 7.0:
        driver_input = state.time/7
    elif state.time <= 22.0:
        driver_input = 1.0
    else:
        driver_input = 0.0

    command_torque = max_torque + driver_input
    force_at_wheels = (command_torque + gear_ratio)/radius
    acceleration = force_at_wheels/radius

    new_vel = state.xvel + acceleration * time_step
    new_xpos = state.xpos + state.xvel * time_step
    new_time = state.time + time_step

# Part 2 Variables
    # IDK if I should put Step 2's variables (slip_angle, lateral_force, etc) into State class, I don't believe we have to since those aren't car properties 
    # Or if I need to adjust some of the attributes instead (xvel -> forward speed and lateral vel)
    # Also DK how to incorporate initialized variables into the model, I believe there are some physics formulas to it
    forward_speed = 15 #Meters/second
    cornering_stiffness = 36000 # Newtons/radians
    # Reserach states that "Cornering stiffness quantifies a tire’s ability to generate lateral force in response to steering input." I require more elaboration. 
    lateral_vel = 0 # Meters/second

# Part 2 Initialization 
    if state.time <= 3:
        steer_angle = 0.08726646 * state.time/3 # 5 degrees converted into 0.087626646 radians
    elif state.time <= 10:
        steer_angle = 0.08726646 # 5 degrees converted into 0.087626646
    else:
        steer_angle = 0

    slip_angle = steer_angle - (lateral_vel/forward_speed)
    lateral_force = cornering_stiffness * slip_angle
    lateral_accel = lateral_force/mass
    lateral_vel = lateral_vel + (lateral_accel * time_step)

# Part 3 Initialization
#IDK how to calculate the variables after 10 seconds, i kind of used A = F/M
    Air_density = 1.2 # kg / meters^3
    Cross_sect_area = 1.2 # meters^2
    drag_coefficient = 0.7 

    Drag = 0.5 * Cross_sect_area * drag_coefficient * Air_density * state.xvel^2

    if state.time <= 10.0:
        acceleration = 5 * state.time/10
    elif state.time > 10 and state.xvel > 0.1:
        acceleration = Drag/mass

    # Net Acceleration should be below the calculation due to the fact that it is based on the calculated and simulated acceleration variable 
    Net_Accel = acceleration - (Drag/mass)
    new_vel = state.xvel + (Net_Accel * time_step)
    new_xpos = state.xpos + state.xvel * time_step
    new_time = state.time + time_step


# Part 4 Initialization
    max_propulsion_force = 2000 # Newtons
    vmax = 27.0 # meters/seconds

    propulsion_force = max_propulsion_force * driver_input * (1 - (state.xvel / vmax))
    acceleration = propulsion_force / mass
    new_vel = state.xvel + (acceleration * time_step)

    if state.time <= 3.0:
        driver_input = state.time/3.0 
    elif state.time <= 23.0:
        driver_input = 1.0
    else:
        driver_input = 0.0

# Part 5 Initialization
# I tested the code just to see what would happen and it seems I have been caught in an infinite loop. My first thought could be that I am not adjusting the time correctly. 
    max_braking_cap = 1850 # Newtons

    Brake_force = driver_input * max_braking_cap
    acceleration = -(Brake_force / mass)
    new_vel = state.xvel + (acceleration * time_step)

    if state.time <= 2.0:
        driver_input = 0.0
        state.xvel = 25.0
    elif state.time > 2.0 and state.xvel > 0.0:
        driver_input = 1.0

    newState = state(
    xpos = new_xpos, 
    ypos = 0.0, 
    xvel = new_vel, 
    time = new_time, 
    )

    return newState

def animate (i):
    global s0
    s0 = step(s0)
    ax.clear()
    ax.scatter([s0.xpos], [s0.ypos], s = 200, c = 'pink', marker = 's')
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 10)
    return ax, 


fig = plt.figure(figsize=(3,3), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
# these lines are so the animation doesnt zoom in or out
plt.pause(3)
ani = animation.FuncAnimation(fig, animate, interval=0)
plt.show()