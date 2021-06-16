import itertools as it
import multiprocessing as mp

import ellipse_functions as ef
import axis_convergence as ac
import numpy as np
import os
from numpy.random import rand

def shell_fit_2D(p, lower_ellipse, sep, guesses_per_branch=50, numiter=2, b_resolution=None, alpha_resolution=2*np.pi/3):
    
    p, a_lower, a_upper, b_lower, b_upper, alpha_upper = _rotate_all(p, lower_ellipse, sep)

    b_resolution = sep if b_resolution is None else b_resolution ; alpha = alpha_upper
    for i in range(numiter):
        
        print(f"iteration {i} \n\tb resolution: \t\t{b_resolution} \n\talpha_resolution: \t{alpha_resolution}")

        #take guesses
        bs, alphas = _generate_guesses(b_upper, b_resolution, alpha_upper, alpha_resolution, guesses_per_branch)

        #test guesses
        b_upper, alpha_upper = _test_guesses(p, a_lower, b_lower, a_upper, bs, alphas)

        #increase resolution
        b_resolution = b_resolution/(guesses_per_branch) ; alpha_resolution = alpha_resolution/(guesses_per_branch)

        print()

    upper_ellipse = (a_upper, b_upper, alpha_upper-alpha)
    return upper_ellipse

def _generate_guesses(b_upper, b_resolution, alpha_upper, alpha_resolution, guesses_per_branch):
    
    bs = np.linspace(b_upper-b_resolution/2+(b_resolution/100), b_upper+b_resolution/2, guesses_per_branch)
    alphas = np.linspace(alpha_upper-alpha_resolution/2, alpha_upper+alpha_resolution/2, guesses_per_branch)
    
    return bs, alphas

def _test_guesses(p, a_lower, b_lower, a_upper, bs, alphas):

    guesses = [x for x in it.product(bs, alphas)]
    res = _run_from_pool(guesses, p, a_lower, b_lower, a_upper)
    best_guess = guesses[res.index(min(res))]
    
    return best_guess
   
def _run_from_pool(guesses, p, a_lower, b_lower, a_upper):
    print(f"\ttesting {len(guesses)} guesses on {os.cpu_count()} cpus")

    args_list = ((p, a_lower, b_lower, a_upper, b_upper, alpha,) for b_upper,alpha in guesses)
    f = _calculate_differences
    with mp.Pool() as pool:
        res = pool.starmap(f, args_list)

    return res

def _calculate_differences(p, a_lower, b_lower, a_upper, b_upper, alpha):

    selection = ef.ellipse_cut(p, (a_lower, b_lower), (a_upper, b_upper, alpha))
    
    M_actual, evecs_actual = ac.iterate_2D(selection)
    M_const, evecs_const = constant_density_eigs((a_lower, b_lower), (a_upper, b_upper, alpha), len(selection)) 

    actual_ratio = M_actual[0]/M_actual[1]
    constant_density_ratio = M_const[0]/M_const[1]

    return np.abs(actual_ratio-constant_density_ratio)

def _rotate_all(p, lower_ellipse, sep):
    a_lower = lower_ellipse[0] ; b_lower = lower_ellipse[1] ; alpha = 0
    a_upper = a_lower + sep ; b_upper = a_upper * b_lower/a_lower 

    if len(lower_ellipse) == 3:
        alpha = lower_ellipse[2]

    p = _rotate_coords(p, alpha)

    return p, a_lower, a_upper, b_lower, b_upper, alpha

def _rotate_coords(pos, alpha):

    R = [[ np.cos(alpha), -np.sin(alpha)],
         [ np.sin(alpha),  np.cos(alpha)]]

    return np.array([np.matmul(p, R) for p in pos])

# returns the expected eigenvalues for a specified shape with constant density
def constant_density_eigs(lower_ellipse, upper_ellipse, num_stars, num_straps=None):
    
    # no error analysis
    if num_straps is None:
        const_density_shape = create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars)
        M, evecs = ac.iterate_2D(const_density_shape)
        return M, evecs

    # parallelized bootstrap
    f = ac.iterate_2D
    const_density_shapes = [[create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars, offset=i/num_straps)]\
                                for i in range(num_straps)]
    with mp.Pool() as pool:
        res = pool.starmap(f, const_density_shapes)

    M_list = np.array([r[0] for r in res]) ; evec_list = np.array([r[1] for r in res])
    return analyze_runs(M_list, evec_list)

def analyze_runs(Ms, evecs):

    M_avg = np.array([np.average(Mi) for Mi in Ms.T])
    vecs_avg = get_average_evecs(evecs)
    uncert = np.array([np.std(Mi) for Mi in Ms.T])

    return M_avg, vecs_avg, uncert

#TODO: implement this
def get_average_evecs(evecs):
    return evecs[0]

# offset: should be less than one, interpreted as the percent offset for one step 
def create_const_density_distribution(lower_ellipse, upper_ellipse, num_stars, offset=0):
    #area to be covered
    A = np.pi * (upper_ellipse[0] * upper_ellipse[1] - lower_ellipse[0] * lower_ellipse[1])
    rho = num_stars/A #<-- number density

    box = create_const_box(max(2*upper_ellipse[0], 2*upper_ellipse[1]), rho, offset)

    return ef.ellipse_cut(box, lower_ellipse, upper_ellipse)

def create_const_box(w, rho, offset=0):

    spacing = w/(int(w*np.sqrt(rho)))
    offset = offset*spacing
    
    x = np.linspace(-w/2-offset, w/2-offset+spacing, int(w*np.sqrt(rho)))
    y = np.linspace(-w/2-offset, w/2-offset+spacing, int(w*np.sqrt(rho)))
    
    #return cartesian coordinates of x and y
    return np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

    


