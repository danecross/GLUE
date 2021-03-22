
filename = "../data/ethan_data/snap.dat.0300"
f = open(filename, 'r')


x = [] ; y = [] ; masses = []
for l in f:
    row = l.split()
    masses += [float(row[2])]
    x += [float(row[2])] ; y += [float(row[3])] 

f.close()

import axis_convergence as ac
import numpy as np

y = list(y - np.average(y))

# split the data into radial cuts

radial_cuts = list(np.load("../data/ethan_data/radii.npy"))
radial_cuts.reverse()

r = np.array([np.sqrt(x[i]**2 + y[i]**2) for i in range(len(x))])
x = np.array([x for _,x in zip(r,x)])
y = np.array([y for _,y in zip(r,y)])

groups = []
lower = 0
for upper in radial_cuts:

    cut = (r<=upper) ; rcut = r[cut] 
    xcut = x[cut] ; ycut = y[cut]
    cut = (rcut>lower)
    xcut = xcut[cut] ; ycut = ycut[cut]

    new_group = [[xcut[i], ycut[i]] for i in range(len(xcut))]
    groups += [new_group]
    
    lower = upper

# analyze each cut

groups = [np.asarray(g) for g in groups]

M = [ac.iterate_2D(group)[0] for group in groups] 
eccentricities = [np.sqrt(1-(m[0]/m[1])**2) for m in M]

np.save("../data/ethan_data/eccentricities.npy", eccentricities)


