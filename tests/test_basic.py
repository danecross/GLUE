
import numpy as np
from numpy.random import normal as norm

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from axis_convergence import _rotate_coords, iterate

np.random.seed(42)

#######################
##   generate case   ##
#######################

# given a set of axes
a = 100. ; b = 20. ; c = 5.
# generate a distribution 
N = 10000
pos = np.ndarray((N, 3))
for i in range(N):
    pos[i,0] = norm(scale=a)
    pos[i,1] = norm(scale=b)
    pos[i,2] = norm(scale=c)

######################
##   test iterate   ##
######################

M, vecs = iterate(pos)

M.sort()
try:
    assert(np.abs(np.sqrt(M[1]/M[2])-b/a)<0.1)
    assert(np.abs(np.sqrt(M[0]/M[2])-c/a)<0.1)
except AssertionError:
    print("--------------------------------------------")
    print("FIRST ITERATION TEST FAILED:")
    print("Final M values:", M)
    print("\ntest | calculated values | expected values | result")
    print("b/c |", np.sqrt(M[1]/M[2]),"|", b/a,"|", np.abs(np.sqrt(M[1]/M[2])-b/a)<0.1)
    print("a/c |", np.sqrt(M[0]/M[2]),"|", c/a,"|", np.abs(np.sqrt(M[0]/M[2])-c/a)<0.1)

###########################
## tilted axes test #######
###########################

#take the data set from before and rotate x-y 45 degrees
rotation_matrix = [[np.cos(np.pi/4), -np.sin(np.pi/4), 0], 
                    [np.sin(np.pi/4), np.cos(np.pi/4), 0], 
                    [0, 0, 1]]

rotated_pos = np.array([np.matmul(rotation_matrix, pos[i]) for i in range(len(pos))])

M_rot, vecs_rot = iterate(rotated_pos)

orig_rotated = np.matmul(rotation_matrix, vecs)

M_rot.sort()
try:
    assert(np.abs(np.sqrt(M_rot[1]/M_rot[2])-b/a)<0.1)
    assert(np.abs(np.sqrt(M_rot[0]/M_rot[2])-c/a)<0.1)
except AssertionError:
    print("--------------------------------------------")
    print("FIRST ITERATION TEST FAILED:")
    print("Final M values:", M_rot)
    print("\ntest | calculated values | expected values | result")
    print("b/c |", np.sqrt(M_rot[1]/M_rot[2]),"|", b/a,"|", np.abs(np.sqrt(M_rot[1]/M_rot[2])-b/a)<0.1)
    print("a/c |", np.sqrt(M_rot[0]/M_rot[2]),"|", c/a,"|", np.abs(np.sqrt(M_rot[0]/M_rot[2])-c/a)<0.1)


print("tests successful")


























