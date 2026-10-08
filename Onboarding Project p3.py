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
    Air_density = 1.2 # kg / meters^3
    Cross_sect_area = 1.2 # meters^2
    drag_coefficient = 0.7 

    if state.time <= 10.0:
        acceleration = 5.0
    elif state.time > 10 and state.xvel > 0.1:
        acceleration = 0.0

    # Net Acceleration should be below the calculation due to the fact that it is based on the calculated and simulated acceleration variable 
    Drag = 0.5 * Cross_sect_area * drag_coefficient * Air_density * state.xvel^2
    Net_Accel = acceleration - (Drag/mass)
    new_vel = state.xvel + (Net_Accel * time_step)
    new_xpos = state.xpos + state.xvel * time_step
    new_time = state.time + time_step

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