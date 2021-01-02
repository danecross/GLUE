
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

t, _, _, p, _ = nb.read_conf3(filepath+"/conf.3_0")
HALF_MASS_RADIUS = np.median([np.sqrt(p[i][0]**2 + p[i][1]**2 + p[i][2]**2) for i in range(len(p))])

if len(sys.argv) > 2:
    chunk = int(sys.argv[2])
    of = int(sys.argv[3])
    
    if chunk > of:
        print("ERROR: sys.argv[2] must be greater than sys.argv[3]")
        exit()

    chunk_len = maxnum//of
    i = chunk_len*(chunk)
    maxnum = chunk_len*(chunk+1)
else:
    i = 0

print("Starting extraction:")

M=[] ; T=[] ; A = [] ; P = []
m_last = [1, 1, 1]
axes_last = [[1,0,0],
             [0,1,0],
             [0,0,1]]
while i < maxnum:
    file_conf3 = filepath+"/conf.3_"+str(i)
    if not os.path.exists(file_conf3):
        i+=1
        continue
    
    t, _, _, p, _ = nb.read_conf3(file_conf3)
    
    #cut stars outside the half mass radius
    p = np.array([p[i] for i in range(len(p)) if np.sqrt(p[i][0]**2 + p[i][1]**2 + p[i][2]**2) <= HALF_MASS_RADIUS])
  
    mm, axes = ac.iterate(p, converge_radius=10e-7, M_last=m_last, evecs_last=axes_last)
    M +=[mm] 
    T += [t]
    m_last = mm ; axes_last = axes

    if i%30==0:
        print(i)
    i+=1

newdir = "../data/pickled_data/"+sys.argv[1]

if len(sys.argv)==2 or not os.path.exists(newdir):
    if os.path.exists(newdir):
        shutil.rmtree(newdir)
    os.mkdir(newdir)

    M = np.array(M)
    T = np.array(T)

else:
    M_old = pickle.load(open(os.path.join(newdir, "M.pkl"), "rb"))
    T_old = pickle.load(open(os.path.join(newdir, "T.pkl"), "rb"))

    start = chunk_len*(chunk)
    i = 0 ; j = 0
    while i < start:
        file_conf3 = filepath+"/conf.3_"+str(i)
        if os.path.exists(file_conf3):
            j+=1
        i+=1
    start_index = j
    end_index = j+len(M)

    if start_index > len(M_old):
        M_old += [0]*(start_index-len(M_old))
        T_old += [0]*(start_index-len(M_old))
    if end_index > len(M_old):
        M_old += [0]*(end_index-len(M_old))
        T_old += [0]*(end_index-len(M_old))
    
    for i in range(start_index, end_index):
        M_old[i] = M[i-start_index]
        T_old[i] = T[i-start_index]

    M = np.array(M_old)
    T = np.array(T_old)


pickle.dump(M, open(os.path.join(newdir, "M.pkl"), "wb"))
pickle.dump(T, open(os.path.join(newdir, "T.pkl"), "wb"))

N = len(p)
cluster_data = np.array([N, HALF_MASS_RADIUS])
pickle.dump(cluster_data, open(os.path.join(newdir, "cluster_data.pkl"), "wb"))




