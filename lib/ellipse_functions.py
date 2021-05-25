
import numpy as np

FULL_THETA = [2*np.pi*(x/100) for x in range(0,101)]

# returns (x, y) coordinates given (r, theta)
def polar_to_cartesian(r, theta):
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return x, y

# returns the eccentricity of an ellipse with 
# (semi-major, semiminor) = (a, b)
def eccentricity(a, b):
    return np.sqrt(1-(b/a)**2)

# returns the distance from the origin for a 
# point on an ellipse and angle theta from 
# x-axis with (semi-major, semiminor) = (a, b)
def r(theta, a, b):
    return a*b/np.sqrt((b*np.cos(theta))**2 + (a*np.sin(theta))**2)

# cuts out all stars within lower_ellipse (with
# semi-major axis a) and all stars outside of 
# the ellipse that has semi-major axis 
# a' = a + diff but the SAME eccentricity
def basic_ellipse_cut(p, lower_ellipse, diff):
    
    a_lower = lower_ellipse[0] ; b_lower = lower_ellipse[1]
    a_upper = a_lower+diff ; b_upper = a_upper*(b_lower/a_lower)

    return ellipse_cut(p, (a_lower, b_lower), (a_upper, b_upper))


# cuts out all stars within lower_ellipse (with
# semi-major axis a) and all stars outside of 
# the ellipse that has semi-major axis 
# a' = a + diff but DIFFERENT eccentricity
def ellipse_cut(p, lower_ellipse, upper_ellipse):

    a_lower = lower_ellipse[0] ; b_lower = lower_ellipse[1]
    a_upper = upper_ellipse[0] ; b_upper = upper_ellipse[1]

    rl = [np.sqrt(x**2 + y**2) for x, y in zip(p[:,0], p[:,1])]
    theta = [np.arctan2(y,x) for x, y in zip(p[:,0], p[:,1])]

    inner_cut = [ ri > r(theta, a_lower, b_lower) for ri, theta in zip(rl, theta)]
    outer_cut = [ ri < r(theta, a_upper, b_upper) for ri, theta in zip(rl, theta)]
   
    cut = [i and o for i,o in zip(inner_cut, outer_cut)]
    
    return p[cut] 


from scipy import integrate
from numpy import sin, cos, pi

# finds the eigenvalues of the mass matrix
# for an ellipse of the given dimensions. Assumes
# constant density
def evals_const_density_full(a, b):
    
    x_result = integrate.quad(f_xx, 0, 2*pi, args = (a, b))
    y_result = integrate.quad(f_yy, 0, 2*pi, args = (a, b))

    return [x_result, y_result]

def f_xx (theta, a, b):

    e = eccentricity(a,b)
    return b**2 * sin(theta)**2 / (1-(e*cos(theta))**2)**2
    
def f_yy (theta, a, b):

    e = eccentricity(a,b)
    return b**2 * cos(theta)**2 / (1-(e*cos(theta))**2)**2

# finds the eigenvalues of the mass matrix 
# for a shell of the given dimensions. Assumes
# constant density
def evals_constant_density_shell(lower_ellipse, upper_ellipse):

    inner_evals = evals_const_density_full(*lower_ellipse)
    outer_evals = evals_const_density_full(*upper_ellipse)

    evals = [outer_evals[i][0]-inner_evals[i][0] for i in range(len(inner_evals))]
    error = [outer_evals[i][1]**2+inner_evals[i][1]**2 for i in range(len(inner_evals))]

    return evals, error





