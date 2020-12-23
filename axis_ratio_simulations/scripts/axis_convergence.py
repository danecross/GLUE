
import numpy as np
from scipy.stats import norm

def q_calc(x, y, z, M):
        ba = np.sqrt(M[0]/M[2])
        bc = np.sqrt(M[1]/M[2])
        return np.array([np.sqrt(x[i]**2 + (y[i]/ba)**2 + (z[i]/bc)**2) for i in range(len(z))])

def M_calc(p, q):

        M = [[np.sum(p[:,i]*p[:,j]/q**2) for j in range(3)] for i in range(3)]
        eigenvalues, eigenvectors = np.linalg.eig(M)

        eigenvalues.sort()

        return eigenvalues, eigenvectors

def iterate(p, M_last=[1, 1, 1], maxiter=10e2, converge_radius=10e-4):
        #starting points
        M = [1, .1, .1]
        q = q_calc(p[:,0], p[:,1], p[:,2], M_last)

        #iterate:
        i = 0
        while (np.abs((M[1]/M[0])-(M_last[1]/M_last[0]))>converge_radius\
                or np.abs((M[2]/M[0])-(M_last[2]/M_last[0])) > converge_radius)\
                and i < maxiter:
                M_last = M
                M, evecs = M_calc(p, q)
                q_last = q
                q = q_calc(p[:,0], p[:,1], p[:,2], M)
                i+=1

        return M, evecs


