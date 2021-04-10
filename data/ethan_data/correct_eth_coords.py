

import numpy as np

filepath = "../data/ethan_data/"
f = open(filepath+"snap.dat.0300", 'r')

corrections = open(filepath+"mcom.dat", 'r')

i=0
while i<299:
    corrections.readline() ; i += 1
corr_row = corrections.readline().split()
corr_x = float(corr_row[0]) ; corr_y = float(corr_row[1])

ln=0
x = [] ; y = [] ; masses = []
for l in f:
    row = l.split()
    masses += [float(row[2])]
    x += [float(row[2])-corr_x] ; y += [float(row[3])-corr_y] 
    ln += 1

f.close()

coords = list(zip(x,y))
np.save("../data/ethan_data/corrected_coords", coords)




