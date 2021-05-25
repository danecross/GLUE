from matplotlib import pyplot as plt
from scipy.optimize import curve_fit, minimize

import ellipse_functions as ef
import axis_convergence as ac
import numpy as np


# returns the expected eigenvalues for a specified shape with constant density
def constant_density_eigs(lower_ellipse, upper_ellipse, num_stars):
    
    const_density_shape = create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars)
    M, evecs = ac.iterate_2D(const_density_shape)

    return M, evecs

def create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars):
    #area to be covered
    A = np.pi * (upper_ellipse[0] * upper_ellipse[1] - lower_ellipse[0] * lower_ellipse[1])
    rho = num_stars/A #<-- number density

    box = create_const_box(2*upper_ellipse[0], 2*upper_ellipse[1], rho)

    return ef.ellipse_cut(box, lower_ellipse, upper_ellipse)

def create_const_box(w, h, rho):

    x = np.linspace(-w/2, w/2, int(w*np.sqrt(rho)))
    y = np.linspace(-h/2, h/2, int(h*np.sqrt(rho)))
    
    #return cartesian coordinates of x and y
    return np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

    


