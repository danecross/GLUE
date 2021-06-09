
import constant_density_shells as cds
from plotting_aid import plot_axes_from_evecs_2D

import sys
import numpy as np
from matplotlib import pyplot as plt
plt.style.use('../../../default_stylesheet.mplstyle')
fig = plt.gcf() ; fig.set_size_inches(50,25)

import os
img_path = "cds_test_rotated_pngs/"
if not os.path.exists(img_path):
    os.mkdir(img_path)


def plot_all(pos, vecs, M, name, a):
    plt.gcf().set_size_inches(20,20)
    plt.plot(pos[:,0], pos[:,1], '.')

    b = a*(M[1]/M[0])**(1/2)
    axes = plot_axes_from_evecs_2D(vecs, [a, b])
    for ax in axes:
        plt.plot(ax[0], ax[1], color="black")

    plt.gca().set_aspect('equal', 'box')
    plt.savefig(name)

#########################
###  create test case ###
#########################

rotation_angle = np.pi/3
lower_ellipse = (10, 5, rotation_angle)
upper_ellipse = (30, 25, rotation_angle)
num_stars = int(sys.argv[1])


################################
##  test create_const_box  #####
################################

height = 20 ; width = 10 ; density = 100

box = cds.create_const_box(max(width, height), density)
plt.plot(box[:,0], box[:,1], '.')
plt.gca().set_aspect('equal', 'box')
plt.savefig(img_path+"const_box_test_" + str(density) + ".png")
plt.cla()

#############################################
##  test create_const_density_distribution ##
#############################################
dist = cds.create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars)
plt.plot(dist[:,0], dist[:,1], '.')
plt.gca().set_aspect('equal', 'box')
plt.savefig(img_path+"const_cutout_test_" + str(num_stars) + ".png")
plt.cla()

################################################
## test constant_density_eigs (basic ellipse) ##
################################################

box = cds.create_const_density_distribution((1e-6,1e-6), upper_ellipse, num_stars)
M, evecs = cds.constant_density_eigs((1e-6,1e-6), upper_ellipse, num_stars)
plot_all(box, evecs, M, img_path+"basic_cde_" + str(num_stars) + ".png", upper_ellipse[0])
plt.cla()


#############################################
## test constant_density_eigs (thin shell) ##
#############################################

thickness = 1

box = cds.create_const_density_distribution((upper_ellipse[0]-thickness*2, upper_ellipse[1]-thickness), upper_ellipse, num_stars)
M, evecs = cds.constant_density_eigs((1e-6,1e-6), upper_ellipse, num_stars)
plot_all(box, evecs, M, img_path+"cde_thin_shell_" + str(num_stars) + ".png", upper_ellipse[0])
plt.cla()


#################################################
## test constant_density_eigs (thin-ish shell) ##
#################################################

box = cds.create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars)
M, evecs = cds.constant_density_eigs((1e-6,1e-6), upper_ellipse, num_stars)
plot_all(box, evecs, M, img_path+"cde_shell_" + str(num_stars) + ".png", upper_ellipse[0])
plt.cla()


#################################################
## test constant_density_eigs (shell series)   ##
#################################################

if not os.path.exists(img_path+"series_" + str(num_stars) + "/"):
    os.mkdir(img_path+"series_" + str(num_stars) + "/")

lower_ellipses = [(15, i, rotation_angle) for i in range(2, 21, 3)]
Ms = []
for lower_ellipse in lower_ellipses:
    box = cds.create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars)
    M, evecs = cds.constant_density_eigs(lower_ellipse, upper_ellipse, num_stars)
    plot_all(box, evecs, M, img_path+"series_" + str(num_stars) + "/cde_shell_" + str(lower_ellipse[1]) + ".png", upper_ellipse[0])
    Ms += [M[0]/M[1]]
    plt.cla()

plt.clf()

plt.style.use('../../../default_stylesheet.mplstyle')
fig = plt.gcf() ; fig.set_size_inches(50,25)

plt.plot([i for i in range(2, 21, 3)], Ms)
plt.title("axis ratios as a function of semi-minor axis")
plt.savefig(img_path+"series_ar_" + str(num_stars) + ".png")

plt.cla()

############################################################
## test constant_density_eigs (shell series, rotations)   ##
############################################################

if not os.path.exists(img_path+"rotated_series_" + str(num_stars) + "/"):
    os.mkdir(img_path+"rotated_series_" + str(num_stars) + "/")

lower_ellipses = [(15, 10, a) for a in np.linspace(0, np.pi, 15)]
Ms = []
for lower_ellipse in lower_ellipses:
    box = cds.create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars)
    M, evecs = cds.constant_density_eigs(lower_ellipse, upper_ellipse, num_stars)
    plot_all(box, evecs, M, img_path+"rotated_series_" + str(num_stars) + "/cde_shell_{x:.2f}.png".format(x=lower_ellipse[2]), upper_ellipse[0])
    Ms += [M[0]/M[1]]
    plt.cla()

plt.clf()

plt.style.use('../../../default_stylesheet.mplstyle')
fig = plt.gcf() ; fig.set_size_inches(50,25)

plt.plot(np.linspace(0, np.pi, 15), Ms)
plt.title("axis ratios as a function of semi-minor axis")
plt.savefig(img_path+"series_ar_rotated_" + str(num_stars) + ".png")


