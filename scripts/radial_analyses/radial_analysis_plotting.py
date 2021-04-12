
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('../../../default_stylesheet.mplstyle')

data_path = "../data/ethan_data/"
eccs1 = np.load(data_path+"eccentricities_1.npy")
radial_divisions1 = np.load(data_path+"radii.npy")

eccs2 = np.load(data_path+"eccentricities_2.npy")
radial_divisions2 = [] ; last_r = 0
for r in radial_divisions1:
    radial_divisions2 += [(last_r+r)/2]
    last_r = r

eccs = [(eccs1[i]+eccs2[i])/2 for i in range(len(eccs1))]

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


plt.plot(radial_divisions1, eccs1, '-o', label="Dubinski & Carlberg")
plt.plot(eth_divisions, eth_eccs, '-o', label="elliptical fit")

plt.title("Eccentricities of Radial Shells")
plt.xlabel("(radius) / (half mass radius)")
plt.ylabel("eccentricity")

plt.legend()

plt.savefig("../plots/ethan_compare/radial_cut_plot.png")

plt.cla()
fig = plt.gcf()
fig.set_size_inches(20, 15)

g = np.load(data_path + "coord_groups.npy", allow_pickle=True)
h = [len(x) for x in g]
divs = list(radial_divisions1) ; divs.reverse()

plt.plot(divs, h)
plt.title("Number of Stars per Bin as a function of Radius")
plt.xlabel("\nRadius")
plt.ylabel("Counts (log scale) \n") ; plt.yscale("log")
plt.savefig('../plots/ethan_compare/bin_distribution.png')




