
import nbody6pp_out as nb
import sys
import os

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

import pickle

filenames = ["0p3", "0p6", "1p2"]

M = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/M.pkl", "rb")) for i in range(len(filenames))]
T = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/T.pkl", "rb")) for i in range(len(filenames))]

names = ["0.3" , "0.6", "1.2"]

for i in range(len(names)):

    a = np.array([M[i][j][0] for j in range(len(M[i]))])
    b = np.array([M[i][j][1] for j in range(len(M[i]))])
    c = np.array([M[i][j][2] for j in range(len(M[i]))])

    fig, ax = plt.subplots(4, 1, sharex=True, sharey=False)
    ax[0].plot(a/c, label="b/a ratio") ; ax[0].set_title("ratios")
    ax[0].plot(b/c, label="c/a ratio") ; ax[0].legend()
    ax[0].set_ylim((0, 1.3))

    ax[1].plot(a) ; ax[1].set_title("a (x-axis)")
    ax[2].plot(b) ; ax[2].set_title("b (y-axis)")
    ax[3].plot(c) ; ax[3].set_title("c (z-axis)")

    fig.tight_layout(pad=3.0)
    plt.savefig("../plots/"+names[i]+"_analysis.png")



