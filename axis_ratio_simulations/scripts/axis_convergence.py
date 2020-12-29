
import numpy as np
from scipy.stats import norm

def q_calc(x, y, z, M):
        ac = np.sqrt(M[0]/M[2])
        bc = np.sqrt(M[1]/M[2])
        return np.array([np.sqrt(x[i]**2 + (y[i]/ac)**2 + (z[i]/bc)**2) for i in range(len(z))])

def M_calc(p, q):

        M = np.zeros((3, 3))
        
        r = np.sqrt((p[:,0])**2 + (p[:,1])**2 + (p[:,2])**2)
        M[0,0] = np.sum(r**2-p[:,0]*p[:,0]/q**2)
        M[0,1] = np.sum(-p[:,0]*p[:,1]/q**2)
        M[0,2] = np.sum(-p[:,0]*p[:,2]/q**2)
        M[1,1] = np.sum(r**2-p[:,1]*p[:,1]/q**2)
        M[1,2] = np.sum(-p[:,1]*p[:,2]/q**2)
        M[2,2] = np.sum(r**2-p[:,2]*p[:,2]/q**2)

        M[1,0]=M[0,1] ; M[2,0]=M[0,2] ; M[2,1]=M[1,2]

        eigenvalues, eigenvectors = np.linalg.eig(M)
        eigenvectors = [x for _,x in sorted(zip(eigenvalues,eigenvectors))]
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


