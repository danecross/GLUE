
import numpy as np
import pickle
from matplotlib import pyplot as plt

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 30, 50
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['font.size'] = 30
mpl.pyplot.title(r'ABC123 vs $\mathrm{ABC123}^{123}$')


cmap = plt.cm.viridis
colors = [cmap(x/10) for x in [3, 6, 9]]

omegas = ['0p3','0p6','1p2']
shells = [(str(x/10), str((x+1)/10)) for x in range(10)]

fig, axs = plt.subplots(10,sharex=True, sharey=True)
data_dir = "../data/pickled_data/{w}_{ls}_{us}_percentile/"

r_h = [2.53, 2.28, 1.64]
i = 0 ; j = 0 
for w in omegas:
    for shell in shells:
        this_dir = data_dir.format(w=w, ls=shell[0], us=shell[1]) 
        M = pickle.load(open(this_dir+"M.pkl", "rb"))
        T = pickle.load(open(this_dir+"T.pkl", "rb"))

        a = np.array([M[j][0] for j in range(len(M))])
        b = np.array([M[j][1] for j in range(len(M))])
        ratio = np.sqrt(a/b)
       
        N = 50000
        hmrt = (0.138)*N*(r_h[i]**(3/2))/np.log(0.11*N)
        x = [T[j]/hmrt for j in range(len(T))]
        
        axs[j].plot(x, ratio,linewidth=0.9,label=shell[0]+"-"+shell[1],
                        color=colors[i])
        j += 1
    '''
    this_dir = data_dir[:-14]+w+"/"
    M = pickle.load(open(this_dir+"M.pkl", "rb"))
    T = pickle.load(open(this_dir+"T.pkl", "rb"))

    a = np.array([M[j][0] for j in range(len(M))])
    b = np.array([M[j][1] for j in range(len(M))])
    ratio = np.sqrt(a/b)
  
    N = 50000
    hmrt = (0.138)*N*(r_h[i]**(3/2))/np.log(0.11*N)
    x = [T[j]/hmrt for j in range(len(T))]

    axs[i].plot(x, ratio,linewidth=0.9,label="total ratios",
                        color='black')
    '''

    j=0
    i+=1

leg = axs[0].legend(bbox_to_anchor=(-0.2, 1), loc='upper left', ncol=1)
fig.tight_layout(pad=1.0)

for legobj in leg.legendHandles:
    legobj.set_linewidth(5.0)

i=0
for ax in axs:
    ax.set_title("shell" + shells[i][0] + "-" + shells[i][1] )
    i+=1

plt.savefig("../plots/percentile_illus_shell_by_shell.png")





