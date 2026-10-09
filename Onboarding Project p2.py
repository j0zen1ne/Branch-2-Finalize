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
    mass = 300 # kg
    forward_speed = 15 #Meters/second
    cornering_stiffness = 36000 # Newtons/radians

    # Part 2 Initialization 
    if state.time <= 3.0:
        steer_angle = 0.08726646 * state.time/3 # 5 degrees converted into 0.087626646 radians
    elif state.time <= 10.0:
        steer_angle = 0.08726646 # 5 degrees converted into 0.087626646 radians
    else:
        steer_angle = 0.0

    slip_angle = steer_angle - (state.xvel/forward_speed)
    lateral_force = cornering_stiffness * slip_angle
    lateral_accel = lateral_force/mass

    new_vel = state.xvel + (lateral_accel * time_step)
    new_xpos = state.xpos + state.xvel * time_step
    new_time = state.time + time_step

    newState = State(
        xpos = new_xpos, 
        ypos = 0.0, 
        xvel = new_vel, 
        time = new_time, 
    )

    return newState

s0 = State(xpos = 0.0, ypos = 0.0, xvel = 0.0, time = 0.0)

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