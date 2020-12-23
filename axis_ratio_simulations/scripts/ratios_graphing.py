
###################
## import data ####
###################
import pickle
import numpy as np

filenames = ["0p3", "0p6", "1p2"]

M = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/M.pkl", "rb")) for i in range(len(filenames))]
T = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/T.pkl", "rb")) for i in range(len(filenames))]

cluster_data = [pickle.load(open("../data/pickled_data/"+ filenames[i] +"/cluster_data.pkl", "rb")) for i in range(len(filenames))]
N = [cluster_data[i][0] for i in range(len(cluster_data))]
r_h = [cluster_data[i][1] for i in range(len(cluster_data))]

names = ["0.3", "0.6", "1.2"]

####################
### plot results ###
####################

import matplotlib.pyplot as plt
import matplotlib as mpl
#mpl.rcParams['figure.figsize'] = 11, 20
#font = {'size'   : 30}
#mpl.rcParams['mathtext.fontset'] = 'stix'
#mpl.rcParams['font.family'] = 'STIXGeneral'

#mpl.rc('font', **font)

fig, ax = plt.subplots(3, 1, sharex=True, sharey=True)

for i in range(len(names)):

    a = [M[i][j][0] for j in range(len(M[i]))]
    b = [M[i][j][1] for j in range(len(M[i]))]
    c = [M[i][j][2] for j in range(len(M[i]))]

    major = [a[j]/c[j] for j in range(len(c))]
    minor = [b[j]/c[j] for j in range(len(a))]

    t = T[i]

    #calculate half mass relaxation time
    hmrt = (0.138)*N[i]*r_h[i]**(3/2)/np.log10(0.11*N[i])
    
    ax[i].plot(minor, label="minor", color="indianred")
    ax[i].plot(major, label="major", color="steelblue")

    ax[i].set_title("$\omega$="+names[i])
#    ax[i].set_ylim(0, 1.3)
ax[0].legend()

plt.suptitle("Axis Ratios for Various Rotations")
plt.savefig("../plots/plotted_ratios.png")
plt.show()




