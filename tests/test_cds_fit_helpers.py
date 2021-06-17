import constant_density_shells as cds
import ellipse_functions as ef

from matplotlib import pyplot as plt
plt.style.use('../../../default_stylesheet.mplstyle')
plt.gca().set_aspect('equal', 'box')
plt.gcf().set_size_inches(20,20)

import numpy as np

img_path = "cds_test_fit_pngs/helper_tests/"

def plot_all(p, lower_ellipse, upper_ellipse, name):
    plt.plot(p[:,0],p[:,1],'.')

    alpha = 0 if len(upper_ellipse)==2 else upper_ellipse[2]

    th = ef.FULL_THETA
    lower_r = ef.r(th, lower_ellipse[0], lower_ellipse[1])
    upper_r = ef.r(th, upper_ellipse[0], upper_ellipse[1], alpha=alpha)

    x_low, y_low = ef.polar_to_cartesian(lower_r, th)
    x_up, y_up = ef.polar_to_cartesian(upper_r, th)

    plt.plot(x_low, y_low, label="lower ellipse")
    plt.plot(x_up, y_up, label="upper fit ellipse")

    plt.legend()
    plt.savefig(img_path+name)


#########################
## create test subject ##
#########################

lower_ellipse = (200, 100, np.pi/6) ; sep = 100
upper_ellipse = (lower_ellipse[0]+2*sep, (lower_ellipse[0]+2*sep)*lower_ellipse[1]/lower_ellipse[0], np.pi/3)
p = cds.create_const_density_distribution(lower_ellipse, upper_ellipse, 3000)

#######################
# test rotate_coords ##
#######################

p0 = cds._rotate_coords(p, np.pi/6)

plt.plot(p[:,0], p[:,1], '.', label="original coordinates")
plt.plot(p0[:,0], p0[:,1], '.', label="rotated coordinates")
plt.legend()

plt.savefig(img_path+"coord_rotations.png")
plt.cla()

#####################
## test rotate_all ##
#####################

p0, a_lower, a_upper, b_lower, b_upper, alpha = cds._rotate_all(p, lower_ellipse, sep, None)
upper_ellipse = (a_upper, b_upper, alpha) ; lower_ellipse = (a_lower, b_lower)
plot_all(p0, lower_ellipse, upper_ellipse, "rotate_all.png")




