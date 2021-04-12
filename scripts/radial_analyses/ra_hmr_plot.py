import numpy as np
import pickle
import matplotlib.pyplot as plt
plt.style.use('../../../default_stylesheet.mplstyle')

data_path = '../data/ethan_data/'

with open(data_path + 'eccentricities_hmr.pkl', 'rb') as handle:
    info_dict = pickle.load(handle)

eccs = info_dict['eccentricities']
radial_divisions = info_dict['radial_divs']

#ethan's data
f = open(data_path+"ethan_analysis.txt", 'r')
eth_eccs = [] ; eth_divisions = []
for line in f:
    if line[0]=='a':
        continue
    datum = line.split()
    eth_divisions += [float(datum[0])]
    eth_eccs += [float(datum[1])]


fig = plt.gcf()
fig.set_size_inches(20, 15)


plt.plot(radial_divisions, eccs, '-o', label="Dubinski & Carlberg")
plt.plot(eth_divisions, eth_eccs, '-o', label="elliptical fit")

plt.title("Eccentricities of Radial Shells")
plt.xlabel("(radius) / (half mass radius)")
plt.ylabel("eccentricity")

plt.legend()

plt.savefig("../plots/ethan_compare/radial_cut_plot_percentile"+str(len(radial_divisions))+".png")

plt.cla()
fig = plt.gcf()
fig.set_size_inches(20, 15)

g = np.load(data_path + "coord_groups.npy", allow_pickle=True)
h = [len(x) for x in g]
divs = list(radial_divisions) ; divs.reverse()

plt.plot(radial_divisions, h)
plt.title("Number of Stars per Bin as a function of Radius")
plt.xlabel("\nRadius")
plt.ylabel("Counts (log scale) \n") ; plt.yscale("log")
plt.savefig('../plots/ethan_compare/bin_distribution_percentile'+str(len(radial_divisions))+'.png')


