
import nbody6pp_out as nb
import sys
import os
import shutil

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

#A = [] ; B = [] ; C = []
#ba = [] ; ca = []
#err_ba = [] ; err_ca = [] 
i = 0 ; T = [] ; M = []
while i < maxnum:
    file_conf3 = filepath+"/conf.3_"+str(i)
    i+=1
    if not os.path.exists(file_conf3):
        continue
    elif i%40 == 0:
        print(i)
    t, _, m, p, _ = nb.read_conf3(file_conf3)
    T += [t]

    a, b, c, err = ac.fast_extract(p)

    M += [[a, b, c]]

#    err_ba += [np.sqrt((err/b)**2 + (err/a)**2)]
#    err_ca += [np.sqrt((err/c)**2 + (err/a)**2)]
#    ba += [b/a]
#    ca += [c/a]


newdir = "../data/pickled_data/"+sys.argv[1]
if not os.path.exists(newdir):
    os.mkdir(newdir)

TT = np.array(T)
pickle.dump(TT, open(os.path.join(newdir, "T.pkl"), "wb"))

M = np.array(M)
pickle.dump(M, open(os.path.join(newdir, "M.pkl"), "wb"))


