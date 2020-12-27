
import sys
import os 
import shutil

import nbody6pp_out as nb
import axis_convergence as ac

import pickle
import numpy as np

if len(sys.argv)==1:
    print("must put omega value to extract. options: 0p6 for 0.6, etc")
    exit()
if sys.argv[1][1]!="p":
    print("must put parseable omega value: e.g. for 0.6 --> 0p6")
    exit()

filepath = "../data/outputs_"+sys.argv[1]+"/conf3s"
if not os.path.exists(filepath):
    print("put the name of the folder")
    print("input:", filepath)
    exit()

#get number of files
dirs = os.listdir(filepath)
for i in range(len(dirs)):
    try:
        dirs[i] = int(dirs[i][7:])
    except:
        dirs[i] = 0
maxnum = max(dirs)

print("Starting extraction:")

i = 0 ; M=[] ; T=[] ; A = [] ; P = []
while i < maxnum:
    file_conf3 = filepath+"/conf.3_"+str(i)
    if not os.path.exists(file_conf3):
        i+=1
        continue
    
    t, _, _, p, _ = nb.read_conf3(file_conf3)
    
    mm, axes = ac.iterate(p, converge_radius=10e-7)
    M +=[mm] 
    T += [t]
    A += [axes]
    P += [p]

    if i%30==0:
        print(i)
    i+=1

newdir = "../data/pickled_data/"+sys.argv[1]
if os.path.exists(newdir):
    shutil.rmtree(newdir)
os.mkdir(newdir)

M = np.array(M)
pickle.dump(M, open(os.path.join(newdir, "M.pkl"), "wb"))

T = np.array(T)
pickle.dump(T, open(os.path.join(newdir, "T.pkl"), "wb"))

A = np.array(A)
pickle.dump(A, open(os.path.join(newdir, "axes.pkl"), "wb"))

HALF_MASS_RADIUS = np.median([np.sqrt(p[i][0]**2 + p[i][1]**2 + p[i][2]**2) for i in range(len(p))])
N = len(p)
cluster_data = np.array([N, HALF_MASS_RADIUS])
pickle.dump(cluster_data, open(os.path.join(newdir, "cluster_data.pkl"), "wb"))

P = np.array(P)
pickle.dump(P, open(os.path.join(newdir, "positions.pkl"), "wb"))













