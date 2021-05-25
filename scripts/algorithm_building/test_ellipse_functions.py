

import numpy as np
import ellipse_functions as ef

theta = ef.FULL_THETA   

# test circle
a = 10 ; b = 10
radii = ef.r(theta, a, b)
for r in radii:
    assert np.abs(r-10)<10e-4

# test ellipse
a = 200 ; b = 100
radii = ef.r(theta, a, b)
x, y = ef.polar_to_cartesian(radii, theta)
for r, xi, yi in zip(radii, x, y):
    assert np.abs(r-(xi**2+yi**2)**(1/2)) < 10e-4

# test conversions
rl = [np.sqrt(xi**2 + yi**2) for xi, yi in zip(x, y)]
theta = [np.arctan2(yi,xi) for xi, yi in zip(x, y)]
xp, yp = ef.polar_to_cartesian(rl, theta)
for r, x, y in zip(radii, xp, yp):
    assert np.abs(r-(x**2+y**2)**(1/2)) < 10e-4


# test eigenvalue finding

#circle: 
a = b = 10
ellipse = [a, b]
result_x, result_y = ef.evals_const_density_full(ellipse)
assert np.abs(result_x[0]-result_y[0]) < result_x[1] + result_y[1]

# ellipse:
a = 20 ; b = 10
ellipse = [a,b]
result_x, result_y = ef.evals_const_density_full(ellipse)

assert np.abs((a/b)**2 - result_x[0]/result_y[0]) < result_x[1] + result_y[1] \
        or np.abs((a/b)**2 - result_y[0]/result_x[0]) < result_x[1] + result_y[1]


