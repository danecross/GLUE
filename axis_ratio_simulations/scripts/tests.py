
import numpy as np
from numpy.random import normal as norm

np.random.seed(42)

########################################
## iterate test                       ##
########################################

from axis_convergence import iterate

# given a set of axes
a = 100 ; b = 30 ; c = 40
# generate a distribution 
N = 10000
pos = np.ndarray((N, 3))
for i in range(N):
        pos[i,0] = norm(scale=a)
        pos[i,1] = norm(scale=b)
        pos[i,2] = norm(scale=c)

#test iterate
M, vecs = iterate(pos, converge_radius=10e-10)

assert(np.abs(np.sqrt(M[1]/M[2])-b/a)<0.2)
assert(np.abs(np.sqrt(M[0]/M[2])-c/a)<0.2)


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

print(orig_rotated)
print(vecs_rot)

'''
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
ax2 = fig.add_subplot(121, projection='3d')

#plot star positions
ax1.plot(pos[:,0], pos[:,1], pos[:,2], '.', markersize=1, color="blue", label="original")
ax2.plot(rotated_pos[:,0], rotated_pos[:,1], rotated_pos[:,2], '.', markersize=1, color='red', label="rotated")

#plot eigenvector axes
a = 100
ax1.plot([-a*vecs[0][0], a*vecs[0][0]], [-a*vecs[0][1], a*vecs[0][1]], [-a*vecs[0][2], a*vecs[0][2]], color="black")
ax1.plot([-a*vecs[1][0], a*vecs[1][0]], [-a*vecs[1][1], a*vecs[1][1]], [-a*vecs[1][2], a*vecs[1][2]], color="black")
ax1.plot([-a*vecs[2][0], a*vecs[2][0]], [-a*vecs[2][1], a*vecs[2][1]], [-a*vecs[2][2], a*vecs[2][2]], color="black")

ax2.plot([-a*vecs_rot[0][0], a*vecs_rot[0][0]], [-a*vecs_rot[0][1], a*vecs_rot[0][1]], [-a*vecs_rot[0][2], a*vecs_rot[0][2]], color="darkblue")
ax2.plot([-a*vecs_rot[1][0], a*vecs_rot[1][0]], [-a*vecs_rot[1][1], a*vecs_rot[1][1]], [-a*vecs_rot[1][2], a*vecs_rot[1][2]], color="darkblue")
ax2.plot([-a*vecs_rot[2][0], a*vecs_rot[2][0]], [-a*vecs_rot[2][1], a*vecs_rot[2][1]], [-a*vecs_rot[2][2], a*vecs_rot[2][2]], color="darkblue")

plt.legend()
plt.show()
'''

print("tests successful")


























