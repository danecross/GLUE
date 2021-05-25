
import numpy as np
from numpy.random import rand
from matplotlib import pyplot as plt

from axis_convergence import _rotate_coords, iterate_2D
import ellipse_functions as ef

np.random.seed(42)

#######################
##   generate case   ##
#######################

# given a set of axes
a = 10. ; b = 5.
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

######################
##   test iterate   ##
######################

M, vecs = iterate_2D(pos)

try:
    assert(np.abs((M[1]/M[0])**(1/2)-b/a)<0.1)
except AssertionError:
    print("--------------------------------------------")
    print("FIRST ITERATION TEST FAILED:")
    print("Final M values:", M)
    print("\ntest | calculated values | expected values | result")
    print("b/a |", np.sqrt(M[1]/M[0]),"|", b/a,"|", np.abs(np.sqrt(M[1]/M[0])-b/a)<0.1)

###########################
## tilted axes test #######
###########################

#take the data set from before and rotate x-y
angle = np.pi/4
rotation_matrix = [[np.cos(angle), -np.sin(angle)], 
                    [np.sin(angle), np.cos(angle)]] 

rotated_pos = np.array([np.matmul(rotation_matrix, pos[i]) for i in range(len(pos))])

M_rot, vecs_rot = iterate_2D(rotated_pos)

orig_rotated = np.matmul(rotation_matrix, vecs)

try:
    assert(np.abs(np.sqrt(M_rot[1]/M_rot[0])-b/a)<0.1)
except AssertionError:

    try: 
        # the axes could have gotten flipped
        assert(np.abs(np.sqrt(M_rot[0]/M_rot[1])-b/a)<0.1)
    except AssertionError:

        print("--------------------------------------------")
        print("SECOND ITERATION TEST FAILED:")
        print("Final M values:", M_rot)
        print("\ntest | calculated values | expected values | result")
        print("b/a |", np.sqrt(M_rot[1]/M_rot[0]),"|", b/a,"|", np.abs(np.sqrt(M_rot[1]/M_rot[0])-b/a)<0.1)


print("tests done")

