
from matplotlib import pyplot as plt
plt.style.use('../../../../../default_stylesheet.mplstyle')
fig = plt.gcf() ; fig.set_size_inches(40,20)

import numpy as np

actual_M = np.load("actual_M.npy", allow_pickle=True)
act_ratios = [(aM[1]/aM[0]) for aM in actual_M]

errs = np.load("errors.npy", allow_pickle=True)
y_errs = [ae*np.sqrt((e[0]/M[0])**2 + (e[1]/M[1])**2) for ae,e,M in zip(act_ratios,errs,actual_M)]

exp_M = np.load("expected_M.npy", allow_pickle=True)
exp_ratios = [(eM[1]/eM[0]) for eM in exp_M]

plt.plot(act_ratios, label="data eigenvalue ratio", color="cornflowerblue")
plt.plot(exp_ratios, label="constant density eigenvalue ratio", color="firebrick")

plt.legend()
plt.title("Compare Ratios btwn Data Cuts and Constant Density Cuts\n")
plt.savefig("ratio_comparison.png")




'''


eth_data = np.load("../../../data/ethan_data/ellipse_specs.npy", allow_pickle=True)
a_s = eth_data[0][::-1] ; b_s = eth_data[1][::-1]
eth_ratios = [b/a for a,b in zip(a_s, b_s)]
eth_eccs = [1-b/a for a,b in zip(a_s, b_s)]

plt.plot(a_s, eth_ratios, label="contour fit ratio", color="firebrick")
p

'''
