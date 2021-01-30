

import numpy as np

# shape 3x64x64x64
grid64 = np.load('SIDM_globular_clusers/lizard/example_scripts/box100/grids/displ_grid_64.npy')


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = [i for i in range(1,65)]*65
for i in range(1,65):
	
z = 
ax.scatter(x, y, z)

plt.savefig("visual.png")
#plt.show()



