
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('../../../default_stylesheet.mplstyle')

data_path = "../data/ethan_data/"
eccs = np.load(data_path+"eccentricities.npy")
radial_divisions = np.load(data_path+"radii.npy")

#ethan's data
f = open(data_path+"ethan_analysis.txt", 'r')
eth_eccs = [] ; eth_divisions = []
for line in f:
    if line[0]=='a':
        continue
    datum = line.split()
    eth_divisions += [float(datum[0])]
    eth_eccs += [float(datum[1])]

# raw plot

fig = plt.gcf()
fig.set_size_inches(20, 15)


plt.plot(radial_divisions, eccs, '-o')
plt.plot(eth_divisions, eth_eccs, '-o')

plt.title("Eccentricities of Radial Shells")
plt.xlabel("(radius) / (half mass radius)")
plt.ylabel("eccentricity")

plt.savefig("../plots/radial_cut_plot.png")



