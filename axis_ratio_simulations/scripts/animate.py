
import sys
sys.path.append('/Users/danecross/Desktop/research/SIDM_glob_clusters/')


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
import os

if len(sys.argv)<2:
    print("ERROR: must input the path to the conf3s")
    exit()

filepath=sys.argv[1]
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
    else:
        x += [p[:,0]]
        y += [p[:,1]]
        if i%100==0:
            print(len(y))

fig = plt.figure()
ax = plt.axes(xlim=(-15, 15), ylim=(-15, 15))
line, = ax.plot([], [], '.', markersize=1)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data(x[i%len(x)], y[i%len(y)])
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=40, blit=True)

plt.show()




