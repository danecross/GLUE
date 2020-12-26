
import sys
sys.path.append('.')


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

filepath="../data/outputs_"+sys.argv[1]+"/conf3s"
dirs = os.listdir(filepath)
for i in range(len(dirs)):
    try:
        dirs[i] = int(dirs[i][7:])
    except:
        dirs[i] = 0
maxnum = max(dirs)

x = None
i = 0 ; T = []
while i < maxnum:
    file_conf3 = filepath+"/conf.3_"+str(i)
    i+=1
    if not os.path.exists(file_conf3):
        continue

    t, _, _, p, _ = nb.read_conf3(file_conf3)
    if x is None:
        x = [p[:,0]]
        y = [p[:,1]]
        z = [p[:,2]]
    else:
        x += [p[:,0]]
        y += [p[:,1]]
        z += [p[:,2]]
        if i%100==0:
            print(len(y))
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
    bodies.set_data(x[i%len(x)], y[i%len(y)])
    bodies.set_3d_properties(z[i%len(z)])

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




