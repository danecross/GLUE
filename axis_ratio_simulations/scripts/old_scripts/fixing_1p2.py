
import nbody6pp_out as nb
import sys
import os

import matplotlib.pyplot as plt
from scipy.stats import norm


import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 11, 20
font = {'size'   : 30}
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.pyplot.title(r'ABC123 vs $\mathrm{ABC123}^{123}$')

mpl.rc('font', **font)



filepath = "outputs_1p2/conf3s"
#get number of files
dirs = os.listdir(filepath)
for i in range(len(dirs)):
    try:
        dirs[i] = int(dirs[i][7:])
    except:
        dirs[i] = 0
maxnum = max(dirs)

ba = [] ; ca = []
xs = [] ; ys = [] ; zs = []
i = 0 ; M=[] ; q=[]
while i < maxnum:
    file_conf3 = filepath+"/conf.3_"+str(i)
    i+=1
    if not os.path.exists(file_conf3):
        continue
    elif i%40 == 0:
        print(i)
    t, _, _, p, _ = nb.read_conf3(file_conf3)

    x = [p[i][0] for i in range(p.shape[0])]
    y = [p[i][1] for i in range(p.shape[0])]
    z = [p[i][2] for i in range(p.shape[0])]

    (mu_x, sigma_x) = norm.fit(x)
    (mu_y, sigma_y) = norm.fit(y)
    (mu_z, sigma_z) = norm.fit(z)
    
    ba += [sigma_y/sigma_x]
    ca += [sigma_z/sigma_x]
    
    xs += [sigma_x]
    ys += [sigma_y]
    zs += [sigma_z]



fig, ax = plt.subplots(4, 1, sharex=True, sharey=True)
ax[0].plot(ba, label="b/a ratio") ; ax[0].set_title("ratios")
ax[0].plot(ca, label="c/a ratio") ; ax[0].legend()
ax[1].plot(xs) ; ax[1].set_title("a (x-axis)")
ax[2].plot(ys) ; ax[2].set_title("b (y-axis)")
ax[3].plot(zs) ; ax[3].set_title("c (z-axis)")

fig.tight_layout(pad=3.0)
plt.savefig("1p2_analysis.png")



