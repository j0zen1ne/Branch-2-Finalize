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
    max_braking_cap = 1850 # Newtons
    mass = 300 # kg

    if state.time <= 2.0:
        driver_input = 0.0
        state.xvel = 25.0
    elif state.time > 2.0 and state.xvel > 0.0:
        driver_input = 1.0
    else:
        driver_input = 0.0

    Brake_force = driver_input * max_braking_cap
    acceleration = -(Brake_force / mass)
    
    new_vel = state.xvel + (acceleration * time_step)
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
    print("At frame ", i, "the velocity is: ", s0.xvel)
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