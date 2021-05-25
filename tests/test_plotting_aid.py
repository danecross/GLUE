

import plotting_aid as pa
import matplotlib.pyplot as plt

img_dir = "plotting_tests/"

#################################
## plot a line from a vector ####

l = pa.line_from_vector([1, 1], 20)

plt.plot(l[0], l[1]) 
plt.savefig(img_dir+"basic_line.png")
plt.gca().set_aspect('equal', 'box')
plt.cla()

#################################

#################################
## plot a set of axes ###########

evecs = [[1, 1], [1, -1]]
length = 20

ls = pa.plot_axes_from_evecs_2D(evecs, length)

for ax in ls:
    plt.plot(ax[0], ax[1])

plt.gca().set_aspect('equal', 'box')
plt.savefig(img_dir+"2D_axes.png")

#################################



