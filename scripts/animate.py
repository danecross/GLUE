
import sys
import numpy as np
import matplotlib.pyplot as plt
import pickle

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 5, 5
font = {'size'   : 10}
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'

mpl.rc('font', **font)

import nbody6pp_out as nb
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import os

if len(sys.argv)<2:
    print("ERROR: must input which omega to animate")
    exit()


#extract axes
lim = 15
filepath = "../data/pickled_data/"+sys.argv[1]+"/axes.pkl"
axes = pickle.load(open(filepath, "rb")) 
x_axes_x = [[-lim*vecs[0][0], lim*vecs[0][0]] for vecs in axes]
y_axes_x = [[-lim*vecs[1][0], lim*vecs[1][0]] for vecs in axes]
z_axes_x = [[-lim*vecs[2][0], lim*vecs[2][0]] for vecs in axes]

x_axes_y = [[-lim*vecs[0][1], lim*vecs[0][1]] for vecs in axes]
y_axes_y = [[-lim*vecs[1][1], lim*vecs[1][1]] for vecs in axes]
z_axes_y = [[-lim*vecs[2][1], lim*vecs[2][1]] for vecs in axes]

x_axes_z = [[-lim*vecs[0][2], lim*vecs[0][2]] for vecs in axes]
y_axes_z = [[-lim*vecs[1][2], lim*vecs[1][2]] for vecs in axes]
z_axes_z = [[-lim*vecs[2][2], lim*vecs[2][2]] for vecs in axes]


#extract positions
filepath = "../data/pickled_data/"+sys.argv[1]+"/positions.pkl"
p = pickle.load(open(filepath, "rb"))

fig = plt.figure() 
ax = plt.axes(xlim=(-lim, lim), ylim=(-lim, lim), projection='3d')
ax.set_zlim3d([-lim, lim])
bodies, = ax.plot([], [], '.', markersize=1)
x_axis, = ax.plot([], [], color="black")
y_axis, = ax.plot([], [], color="black")
z_axis, = ax.plot([], [], color="black")

def init():
    bodies.set_data([], []) ; bodies.set_3d_properties([])
    x_axis.set_data([], []) ; x_axis.set_3d_properties([])
    y_axis.set_data([], []) ; y_axis.set_3d_properties([])
    z_axis.set_data([], []) ; z_axis.set_3d_properties([])

    return bodies, x_axis, y_axis, z_axis,

def animate(i):

    x = [p[i][j][0] for j in range(len(p[i]))]
    y = [p[i][j][1] for j in range(len(p[i]))]
    z = [p[i][j][2] for j in range(len(p[i]))]

    bodies.set_data(x, y)
    bodies.set_3d_properties(z)

    x_axis.set_data(x_axes_x[i%len(x)], x_axes_y[i%len(x)]) 
    x_axis.set_3d_properties(x_axes_z[i%len(x)])

    y_axis.set_data(y_axes_x[i%len(x)], y_axes_y[i%len(x)])
    y_axis.set_3d_properties(y_axes_z[i%len(x)])

    z_axis.set_data(z_axes_x[i%len(x)], z_axes_y[i%len(x)])
    z_axis.set_3d_properties(z_axes_z[i%len(x)])
    
    return bodies, x_axis, y_axis, z_axis,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=1000, blit=True)

plt.show()



