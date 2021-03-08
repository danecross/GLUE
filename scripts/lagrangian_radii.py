

import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 18, 20
font = {'size'   : 30}
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.pyplot.title(r'ABC123 vs $\mathrm{ABC123}^{123}$')

mpl.rc('font', **font)

cmap = plt.cm.viridis
colors = [cmap(x/11) for x in range(11)]

omegas = ['1p2', '0p6', '0p3'] ; omegas.reverse() 
fig, axs = plt.subplots(3)
fig.tight_layout(pad=3.0)

j = 0
r_h = [2.53, 2.28, 1.64]
for w in omegas:
    lagr_file = "../data/lagragian_radii/lagr.7_"+w
    f = open(lagr_file, "r")
    # get percentages
    f.readline()
    header = f.readline().split()
    percents = [float(header[i]) for i in range(1,12)]
    
    T = [] ; LR = [[] for _ in range(11)]
    for line in f:
        row = line.split()
        if line[0]=="#" or line[0]=="T":
            continue
    
        row = [float(e) for e in row]

        for i in range(1,12): 
            LR[i-1].append(row[i])
    
        time = row[0]
        T.append(time)
    
    k = 0
    for l in LR:
        hmrt = (0.138)*50000*(r_h[j]**(3/2))/np.log(0.11*50000)
        x = [T[i]/hmrt for i in range(len(T))]
    
        axs[j].plot(x, l, color=colors[k], label=percents[k])
        k += 1

    axs[j].set_title(w)
    axs[j].set_yscale("log")
    j+=1

axs[2].set_xlabel("Half-Mass Relaxation Time")
plt.suptitle("Lagrangian Radii of Different Initial Rotations")
leg = axs[0].legend(loc=(1.04, -1.5))

fig.subplots_adjust(right=0.8)

#plt.show()
plt.savefig("../plots/lagrangian_radii.png")




