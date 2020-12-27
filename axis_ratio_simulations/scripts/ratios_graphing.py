
#TODO
# change the time axes to half mass relaxation time so you know if you just need to run the simulations for much longere

import sys
sys.path.append('/Users/danecross/Desktop/research/SIDM_glob_clusters/')
import os
import nbody6pp_out as nb

import numpy as np

import matplotlib.pyplot as plt
from scipy.stats import norm


import matplotlib as mpl
mpl.rcParams['figure.figsize'] = 11, 20
font = {'size'   : 30}
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.pyplot.title(r'ABC123 vs $\mathrm{ABC123}^{123}$')

mpl.rc('font', **font)
colors=['firebrick', 'mediumaquamarine', 'goldenrod']

import pickle

filenames = ["0p3", "0p6", "1p2"]

M = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/M.pkl", "rb")) for i in range(len(filenames))]
T = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/T.pkl", "rb")) for i in range(len(filenames))]

# half-mass relaxation data for the x-axis
cluster_data = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/cluster_data.pkl", "rb")) for i in range(len(filenames))]
N = [cluster_data[i][0] for i in range(len(cluster_data))]
r_h = [cluster_data[i][1] for i in range(len(cluster_data))]

fig_full, ax_full = plt.subplots(3, 1, sharex=True, sharey=True)
fig_full.set_size_inches(20, 20)

names = ["0.3" , "0.6", "1.2"] 
for i in range(len(names)):

    hmrt = (0.138)*N[i]*r_h[i]**(3/2)/np.log10(0.11*N[i])
    x = [T[i][j]/hmrt for j in range(len(T[i]))]

    a = np.array([M[i][j][0] for j in range(len(M[i]))])
    b = np.array([M[i][j][1] for j in range(len(M[i]))])
    c = np.array([M[i][j][2] for j in range(len(M[i]))])

    print(len(x), len(a))
    
    fig, ax = plt.subplots(4, 1, sharex=True, sharey=False)
    ax[0].plot(x, a/c, label="b/a ratio", color=colors[0]) ; ax[0].set_title("ratios")
    ax[0].plot(x, b/c, label="c/a ratio", color=colors[1]) ; ax[0].legend()
    ax[0].set_ylim((0, 1.3))

    ax[1].plot(x, a, color=colors[0]) ; ax[1].set_title("a (x-axis)")
    ax[2].plot(x, b, color=colors[1]) ; ax[2].set_title("b (y-axis)")
    ax[3].plot(x, c, color=colors[2]) ; ax[3].set_title("c (z-axis)")

    fig.tight_layout(pad=3.0)
    plt.savefig("../plots/"+names[i]+"_analysis.png")

    ax_full[i].set_title(names[i])
    ax_full[i].plot(x, a/c, label="b/a ratio", color=colors[0])
    ax_full[i].plot(x, b/c, label="c/a ratio", color=colors[1])

    #orig = ax_full[i].get_xticks()
    #new = [int(float(orig[j])/hmrt[i]) for j in range(len(orig))]
    #ax_full[i].set_xticks(new)


ax_full[2].legend(bbox_to_anchor=(0.5, -0.6), loc='lower center')
fig_full.tight_layout(pad=3.0)
fig_full.savefig("../plots/plotted_ratios.png")

