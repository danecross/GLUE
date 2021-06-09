
import axis_convergence as ac
import numpy as np


# returns the eigenvalues, eigenvectors, and separated coordinates 
# of groups of stars from a snapshot. The groups are radial cuts
# of the data in the snapshot

def eigen_analyze_cuts(radial_cuts, x, y):
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

    results = [ac.iterate_2D(group) for group in groups]

    M = [results[i][0] for i in range(len(results))]
    evecs = [results[i][1] for i in range(len(results))]

    return M, evecs, groups

def eigen_analyze_cuts(x, y, hmr=None, n_divs=1, is_percentile=False):

    p = np.array(list(zip(x,y))) 
    groups = [ac.get_stars(p, lower_shell=x*(1/n_divs), upper_shell=(x+1)*(1/n_divs), \
                is_percentile=is_percentile) for x in range(0,n_divs)]
    
    results = [ac.iterate_2D(group) for group in groups]

    M = [results[i][0] for i in range(len(results))]
    evecs = [results[i][1] for i in range(len(results))]
    
    return M, evecs, groups




