
import sys
import os 
import shutil

import nbody6pp_out as nb
import axis_convergence as ac

import pickle
import numpy as np

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("omega", help="omega value to extract. options: [0p3, 0p6, 1p2]", type=str)
parser.add_argument("--lower_shell", help="lower shell percentage", default=0.0, type=float)
parser.add_argument("--upper_shell", help="upper shell percentage", default=1.0, type=float)
args = parser.parse_args()

omega = args.omega
lower_shell = args.lower_shell
upper_shell = args.upper_shell
print(omega, lower_shell, upper_shell)

if lower_shell >= upper_shell:
    print("error: lower_shell value must be smaller than upper_shell")
    exit()

filepath = "../data/outputs_"+sys.argv[1]+"/conf3s"
if not os.path.exists(filepath):
    print("put the name of the folder where the conf3s are")
    print("input:", filepath)
    exit()

#get number of files
dirs = os.listdir(filepath)
conf3_numbers = [int(d[7:]) for d in dirs if d[7:].isdigit()]
maxnum = max(conf3_numbers)

t, _, _, p, _ = nb.read_conf3(filepath+"/conf.3_0")
HALF_MASS_RADIUS = np.median([np.sqrt(p[i][0]**2 + p[i][1]**2 + p[i][2]**2) for i in range(len(p))])

print("Starting extraction:")

M, T = ac.extract_ratios(filepath, maxnum, HALF_MASS_RADIUS, lower_shell=lower_shell, upper_shell=upper_shell)
M = np.array(M)
T = np.array(T)

newdir = "../data/pickled_data/"+sys.argv[1]
if os.path.exists(newdir):
    shutil.rmtree(newdir)
os.mkdir(newdir)

pickle.dump(M, open(os.path.join(newdir, "M.pkl"), "wb"))
pickle.dump(T, open(os.path.join(newdir, "T.pkl"), "wb"))

N = len(p)
cluster_data = np.array([N, HALF_MASS_RADIUS])
pickle.dump(cluster_data, open(os.path.join(newdir, "cluster_data.pkl"), "wb"))




