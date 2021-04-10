
import axis_convergence as ac
import numpy as np

def get_eccentricities(radial_cuts, x, y):
    r = np.array([np.sqrt(x[i]**2 + y[i]**2) for i in range(len(x))])
    x_sort = np.array([x for _,x in zip(r,x)])
    y_sort = np.array([y for _,y in zip(r,y)])

    groups = []
    lower = 0
    for upper in radial_cuts:

        cut = (r<=upper) ; rcut = r[cut]
        xcut = x_sort[cut] ; ycut = y_sort[cut]
        cut = (rcut>lower)
        xcut = xcut[cut] ; ycut = ycut[cut]

        new_group = [[xcut[i], ycut[i]] for i in range(len(xcut))]
        groups += [new_group]

        lower = upper

    # analyze each cut

    groups = [np.asarray(g) for g in groups]

    M = [ac.iterate_2D(group)[0] for group in groups]
    eccentricities = [1-(m[0]/m[1]) for m in M]

    return eccentricities, groups

def get_eccentricities(x, y, hmr=None, n_divs=1, is_percentile=False):

    p = np.array(list(zip(x,y))) 
    groups = [ac.get_stars(p, lower_shell=x*(1/n_divs), upper_shell=(x+1)*(1/n_divs), \
                is_percentile=is_percentile) for x in range(0,n_divs)]
    
    M = [ac.iterate_2D(group)[0] for group in groups]
    eccentricities = [1-(m[0]/m[1]) for m in M]

    return eccentricities, groups



