import ellipse_functions as ef
import constant_density_shells as cds
import axis_convergence as ac

import numpy as np
from matplotlib import pyplot as plt

def plot_all(p, lower_ellipse, upper_ellipse, name):
    plt.plot(p[:,0],p[:,1],'.', markersize=1)

    alpha = 0 if len(upper_ellipse)==2 else upper_ellipse[2]

    th = ef.FULL_THETA
    lower_r = ef.r(th, lower_ellipse[0], lower_ellipse[1])
    upper_r = ef.r(th, upper_ellipse[0], upper_ellipse[1], alpha=alpha)

    x_low, y_low = ef.polar_to_cartesian(lower_r, th)
    x_up, y_up = ef.polar_to_cartesian(upper_r, th)

    plt.plot(x_low, y_low, label="lower ellipse")
    plt.plot(x_up, y_up, label="upper fit ellipse")

    plt.legend()
    plt.show()
    #plt.savefig(img_path+name)


contour_fit_info = np.load("../../../data/ethan_data/ellipse_specs.npy")
a_s = contour_fit_info[0] ; b_s = contour_fit_info[1] ; alpha_s = contour_fit_info[2]

p = np.load("../../../data/ethan_data/corrected_coords.npy", allow_pickle=True)
p = np.array(p)

expected_ratios = [] ; actual_ratios = []
expected_evals = [] ; actual_evals = []
errs = []
i = list(a_s).index(min(a_s))
lower_ellipse = (a_s[i], b_s[i], alpha_s[i])
for upper_ellipse in sorted(zip(a_s, b_s, alpha_s))[1:]:

    selection = ef.ellipse_cut(p, lower_ellipse, upper_ellipse) 

    M_actual, evecs_actual = ac.iterate_2D(selection)
    M_exp, evecs_exp, errors = cds.constant_density_eigs(lower_ellipse, upper_ellipse, len(selection), num_straps=5) 

    expected_ratios += [M_exp]
    actual_ratios += [M_actual]

    expected_evals += [evecs_exp]
    actual_evals += [evecs_actual]

    errs += [errors]

expected_ratios = np.array(expected_ratios)
actual_ratios = np.array(actual_ratios)
expected_evals = np.array(expected_evals)
actual_evals = np.array(actual_evals)
errs = np.array(errs)

np.save("actual_M.npy",actual_ratios)
np.save("expected_M.npy",expected_ratios)
np.save("expected_evals.npy",expected_evals)
np.save("actual_evals.npy",actual_evals)
np.save("errors.npy",errs)
