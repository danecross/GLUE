import numpy as np
from matplotlib import pyplot as plt
plt.style.use('../../../default_stylesheet.mplstyle')
plt.gca().set_aspect('equal', 'box')
plt.gcf().set_size_inches(20,20)

import constant_density_shells as cds
import ellipse_functions as ef

img_path = "cds_test_fit_pngs/"

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



##########################
## test basic shell fit ##
##########################

lower_ellipse = (200, 100) ; sep = 100
upper_ellipse = (lower_ellipse[0]+sep, (lower_ellipse[0]+sep)*lower_ellipse[1]/lower_ellipse[0])
p = cds.create_const_density_distribution(lower_ellipse, upper_ellipse, 3000)

lower_ellipse = (90, 90) ; sep = 150
upper_ellipse_fit = cds.shell_fit_2D(p, lower_ellipse, sep, parallelize=True)
plot_all(p, lower_ellipse, upper_ellipse_fit, "fit_basic.png")
plt.cla()

############################
## test rotated shell fit ##
############################

lower_ellipse = (200, 100, np.pi/6) ; sep = 100
upper_ellipse = (lower_ellipse[0]+sep, (lower_ellipse[0]+sep)*lower_ellipse[1]/lower_ellipse[0], np.pi/3)
p = cds.create_const_density_distribution(lower_ellipse, upper_ellipse, 3000)

lower_ellipse = (90, 90) ; sep = 150
upper_ellipse_fit = cds.shell_fit_2D(p, lower_ellipse, sep)
print("ellipse:", upper_ellipse_fit)

plot_all(p, lower_ellipse, upper_ellipse_fit, "fit_rotated.png")




























