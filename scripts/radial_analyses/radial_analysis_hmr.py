
import pickle
import numpy as np
from snapshot_analysis import get_eccentricities


coords = np.load("../data/ethan_data/corrected_coords.npy", allow_pickle=True)
x = [coords[i][0] for i in range(len(coords))]
y = [coords[i][1] for i in range(len(coords))]

# radial cuts in terms of 1/nth mass radius
eccs, grps = get_eccentricities(x, y, n_divs=14, is_percentile=True)

divs = []
for group in grps:
    boundary = group[0] ; x = boundary[0] ; y = boundary[1]
    divs += [np.sqrt(x**2 + y**2)]
    print(boundary, np.sqrt(x**2 + y**2))
    
info_dict = {"eccentricities"   : eccs, 
             "radial_divs"      : divs}

with open('../data/ethan_data/eccentricities_hmr.pkl', 'wb') as handle:
    b = pickle.dump(info_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

np.save("../data/ethan_data/coord_groups.npy", grps)



