import itertools as it
import multiprocessing as mp

import ellipse_functions as ef
import axis_convergence as ac
import numpy as np
from numpy.random import rand

def shell_fit_2D(p, lower_ellipse, sep, guesses_per_branch=10, numiter=2, parallelize=False):
    
    p, a_lower, a_upper, b_lower, b_upper, alpha_upper = rotate_all(p, lower_ellipse, sep)

    b_resolution = sep ; alpha_resolution = 2*np.pi/3 ; alpha = alpha_upper
    for _ in range(numiter):

        #take guesses
        rand_bs, rand_alphas = generate_guesses(b_upper, b_resolution, alpha_upper, alpha_resolution, guesses_per_branch)
        guesses = [guess for guess in it.product(rand_bs, rand_alphas)]

        #test guesses
        if parallelize: diffs = test_guesses_parallel(p, a_lower, b_lower, a_upper, guesses)
        else: diffs = [calculate_differences(p, a_lower, b_lower, a_upper, b_upper, alpha) for b_upper, alpha in guesses]

        # establish best fit b and increase resolution
        i = diffs.index(min(diffs))
        b_upper = guesses[i][0] ; alpha_upper = guesses[i][1]

        b_resolution = b_resolution/(guesses_per_branch) ; alpha_resolution = alpha_resolution/(guesses_per_branch)

    upper_ellipse = (a_upper, b_upper, alpha_upper-alpha)
    return upper_ellipse

def test_guesses_parallel(p, a_lower, b_lower, a_upper, guesses):

    f = calculate_differences 
    args_list = ((p, a_lower, b_lower, a_upper, b_upper, alpha,) \
                    for b_upper, alpha in guesses)

    with mp.Pool() as pool:
        res = pool.starmap(f, args_list)
    
    return res

def generate_guesses(b_upper, b_resolution, alpha_upper, alpha_resolution, guesses_per_branch):
    
    rand_bs = [b_upper + 2*(rand()-0.5)*b_resolution for i in range(guesses_per_branch)]
    rand_alphas = [alpha_upper + 2*(rand()-0.5)*alpha_resolution for i in range(guesses_per_branch)]

    return rand_bs, rand_alphas

def calculate_differences(p, a_lower, b_lower, a_upper, b_upper, alpha):

    selection = ef.ellipse_cut(p, (a_lower, b_lower), (a_upper, b_upper, alpha))
    
    M_actual, evecs_actual = ac.iterate_2D(selection)
    M_const, evecs_const = constant_density_eigs((a_lower, b_lower), (a_upper, b_upper, alpha), len(selection)) 

    actual_ratio = M_actual[0]/M_actual[1]
    constant_density_ratio = M_const[0]/M_const[1]

    return actual_ratio-constant_density_ratio

def rotate_all(p, lower_ellipse, sep):
    a_lower = lower_ellipse[0] ; b_lower = lower_ellipse[1] ; alpha = 0
    a_upper = a_lower + sep ; b_upper = a_upper * b_lower/a_lower 

    if len(lower_ellipse) == 3:
        alpha = lower_ellipse[2]

    p = rotate_coords(p, alpha)

    return p, a_lower, a_upper, b_lower, b_upper, alpha

def rotate_coords(pos, alpha):

    R = [[ np.cos(alpha), -np.sin(alpha)],
         [ np.sin(alpha),  np.cos(alpha)]]

    return np.array([np.matmul(p, R) for p in pos])


# returns the expected eigenvalues for a specified shape with constant density
def constant_density_eigs(lower_ellipse, upper_ellipse, num_stars):
    
    const_density_shape = create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars)
    M, evecs = ac.iterate_2D(const_density_shape)

    return M, evecs

def create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars):
    #area to be covered
    A = np.pi * (upper_ellipse[0] * upper_ellipse[1] - lower_ellipse[0] * lower_ellipse[1])
    rho = num_stars/A #<-- number density

    box = create_const_box(max(2*upper_ellipse[0], 2*upper_ellipse[1]), rho)

    return ef.ellipse_cut(box, lower_ellipse, upper_ellipse)

def create_const_box(w, rho):

    x = np.linspace(-w/2, w/2, int(w*np.sqrt(rho)))
    y = np.linspace(-w/2, w/2, int(w*np.sqrt(rho)))
    
    #return cartesian coordinates of x and y
    return np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

    


