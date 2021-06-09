
from matplotlib import pyplot as plt
plt.style.use('../../../../../default_stylesheet.mplstyle')
fig = plt.gcf() ; fig.set_size_inches(50,25)

import numpy as np

expected_M = np.load("expected_M.npy", allow_pickle=True)
actual_M = np.load("actual_M.npy", allow_pickle=True)

exp_ratios = [eM[1]/eM[0] for eM in expected_M]
act_ratios = [(aM[1]/aM[0])**2 for aM in actual_M]

plt.plot(exp_ratios, label="contour ratios")
plt.plot(act_ratios, label="eigen ratios")
plt.legend()
plt.savefig("ratio_comparison.png")





