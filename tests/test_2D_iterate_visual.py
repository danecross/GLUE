

import numpy as np
from numpy.random import rand

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from axis_convergence import _rotate_coords, iterate_2D
from plotting_aid import plot_axes_from_evecs_2D
import ellipse_functions as ef

plt.style.use('../../../../default_stylesheet.mplstyle')
plt.gcf().set_size_inches(20,20)

np.random.seed(42)

image_dir = 'iterate_test_pngs/'

def plot_all(pos, vecs, M, name, a):
    plt.gcf().set_size_inches(20,20)
    plt.plot(pos[:,0], pos[:,1], '.')

    b = a*(M[1]/M[0])**(1/2)
    axes = plot_axes_from_evecs_2D(vecs, [a, b])
    for ax in axes:
        plt.plot(ax[0], ax[1], color="black")
    
    plt.gca().set_aspect('equal', 'box')
    plt.savefig(image_dir+name+".png")


#######################
##   generate case   ##
#######################

# given a set of axes
a = 20. ; b = 10. 
# generate a distribution 
N = 10000
pos = np.ndarray((N, 2))
i = 0 
while i < N:
    x = 2*(rand()-0.5)*a ; y = 2*(rand()-0.5)*b
    r = np.sqrt(x**2 + y**2) ; th = np.arctan2(y,x)
    if r < ef.r(th, a, b):
        pos[i,0] = x ; pos[i,1] = y
        i += 1

# plot_all test
a,b = (20,10)
vecs = [[1,0],[0,1]]
M = [200**2, 100**2]
axes = plot_all(pos, vecs, M, "testi.png", a)

######################
##   test iterate   ##
######################

M, vecs = iterate_2D(pos)

plot_all(pos, vecs, M, "2D_axes_basic", a)

###########################
## tilted axes test #######
###########################

#take the data set from before and rotate x-y 45 degrees
rotation_matrix = [[np.cos(np.pi/4), -np.sin(np.pi/4)],
                    [np.sin(np.pi/4), np.cos(np.pi/4)]]

rotated_pos = np.array([np.matmul(rotation_matrix, v) for v in pos])

M_rot, vecs_rot = iterate_2D(rotated_pos)

plt.cla()
plot_all(rotated_pos, vecs_rot, M_rot, "2D_axes_rotated", a)

#################


####################################
## series of fits visualizations ###
####################################

a = 10
xx = [] ; MM = [] ; ba = []
for b in range(1,31):
    i = 0 
    while i < N:
        x = 2*(rand()-0.5)*a ; y = 2*(rand()-0.5)*b
        r = np.sqrt(x**2 + y**2) ; th = np.arctan2(y,x)
        if r < ef.r(th, a, b):
            pos[i,0] = x ; pos[i,1] = y
            i += 1

    M, vecs = iterate_2D(pos)

    plt.cla()
    plot_all(pos, vecs, M, "multi_run/multi_run_"+str(b), a)

    xx += [b]
    MM += [(M[1]/M[0])**(1/2)]
    ba += [b/a]

plt.cla() ; plt.gca().set_aspect('auto')
plt.title("Difference of Ratios with a = "+str(a))
plt.plot(xx, MM, label="calculated ratio")
plt.plot(xx, ba, label="expected ratio")
plt.xlabel("b") 
plt.legend()
plt.savefig(image_dir+"ratio_difference.png")

np.save(image_dir+"calculated_ratios.npy", MM)
np.save(image_dir+"expected_ratios.npy", ba)
np.save(image_dir+"b-values.npy", xx)



