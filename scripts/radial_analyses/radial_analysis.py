import numpy as np
from snapshot_analysis import get_eccentricities

coords = np.load("../data/ethan_data/corrected_coords.npy", allow_pickle=True)
x = [coords[i][0] for i in range(len(coords))]
y = [coords[i][1] for i in range(len(coords))]

# split the data into radial cuts

radial_cut_1 = list(np.load("../data/ethan_data/radii.npy"))
radial_cut_1.reverse()
eccs1, _ = get_eccentricities(radial_cut_1, x, y)
np.save("../data/ethan_data/eccentricities_1.npy", eccs1)

radial_cut_2 = [] ; last_r = 0
for r in radial_cut_1:
    radial_cut_2 += [(last_r+r)/2]
    last_r = r
eccs2, g = get_eccentricities(radial_cut_2, x, y)
np.save("../data/ethan_data/eccentricities_2.npy", eccs2)
np.save("../data/ethan_data/coord_groups.npy", g)

