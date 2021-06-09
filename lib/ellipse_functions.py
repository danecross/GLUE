
import numpy as np
from numpy import cos, sin

FULL_THETA = np.array([2*np.pi*(x/100) for x in range(0,101)])

# returns (x, y) coordinates given (r, theta)
def polar_to_cartesian(r, theta):
    x = r*cos(theta)
    y = r*sin(theta)
    return x, y

# returns the eccentricity of an ellipse with 
# (semi-major, semiminor) = (a, b)
def eccentricity(a, b):
    return np.sqrt(1-(b/a)**2)

# returns the distance from the origin for a 
# point on an ellipse and angle theta from 
# x-axis with (semi-major, semiminor) = (a, b)
def r(theta, a, b, alpha=0):
    return a*b/np.sqrt((b*np.cos(theta-alpha))**2 + (a*np.sin(theta-alpha))**2) 
    
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
def ellipse_cut(p, lower_ellipse, upper_ellipse, center=(0,0)):

    a_lower = lower_ellipse[0] ; b_lower = lower_ellipse[1] ; alpha_lower = 0
    a_upper = upper_ellipse[0] ; b_upper = upper_ellipse[1] ; alpha_upper = 0

    if len(lower_ellipse) == 3:
        alpha_lower = lower_ellipse[2]
    if len(upper_ellipse) == 3:
        alpha_upper = upper_ellipse[2]

    cx, cy = center
    x = p[:,0]+cx ; y = p[:,1]+cy
    rl = [np.sqrt(x**2 + y**2) for x, y in zip(x, y)]
    theta = [np.arctan2(y,x) for x, y in zip(x, y)]

    inner_cut = [ ri > r(theta, a_lower, b_lower, alpha=alpha_lower) for ri, theta in zip(rl, theta)]
    outer_cut = [ ri < r(theta, a_upper, b_upper, alpha=alpha_upper) for ri, theta in zip(rl, theta)]
   
    cut = [i and o for i,o in zip(inner_cut, outer_cut)]
   
    return p[cut] 


from scipy import integrate
from numpy import sin, cos, pi

# finds the eigenvalues of the mass matrix
# for an ellipse of the given dimensions. Assumes
# constant density and no rotation angle for ellipses
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





