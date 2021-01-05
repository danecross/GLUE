
import numpy as np
from scipy.stats import norm

def _q_calc(x, y, z, M):
    
    M.sort()
    ac = np.sqrt(M[0]/M[2])
    bc = np.sqrt(M[1]/M[2])

    return np.array([np.sqrt(x[i]**2 + (y[i]/ac)**2 + (z[i]/bc)**2) for i in range(len(z))])

def _M_calc(p, q):

        M = np.zeros((3, 3))
       
        M[0,0] = np.sum(p[:,0]*p[:,0]/q**2)
        M[0,1] = np.sum(p[:,0]*p[:,1]/q**2)
        M[0,2] = np.sum(p[:,0]*p[:,2]/q**2)
        M[1,1] = np.sum(p[:,1]*p[:,1]/q**2)
        M[1,2] = np.sum(p[:,1]*p[:,2]/q**2)
        M[2,2] = np.sum(p[:,2]*p[:,2]/q**2)

        M[1,0]=M[0,1] ; M[2,0]=M[0,2] ; M[2,1]=M[1,2]

        eigenvalues, eigenvectors = np.linalg.eig(M)
        
        return np.array(eigenvalues), eigenvectors

def _rotate_coords(evecs, p):
    vec_new = [np.linalg.inv(np.array(evecs)).dot(coord) for coord in p]
    return np.array(vec_new)

empty_coords = [[1,0,0],
                [0,1,0],
                [0,0,1]]

def iterate(p, M_last=[1, 1, 1], evecs_last=empty_coords, maxiter=25, converge_radius=10e-4):
        #starting points
        M = [1, .1, .1]
        p = _rotate_coords(evecs_last, p)
        q = _q_calc(p[:,0], p[:,1], p[:,2], M_last)

        # re-center coordinates
        center = [np.average(p[:,0]), np.average(p[:,1]), np.average(p[:,2])]
        p = np.array([[p[i,0]-center[0], p[i,1]-center[1], p[i,2]-center[2]] for i in range(len(p))])

        #iterate:
        i = 0
        while (np.abs((M[1]/M[0])-(M_last[1]/M_last[0]))>converge_radius\
                or np.abs((M[2]/M[0])-(M_last[2]/M_last[0])) > converge_radius)\
                and i < maxiter:
                M_last = M
                M, evecs = _M_calc(p, q)
                q_last = q
                p = _rotate_coords(evecs, p)
                q = _q_calc(p[:,0], p[:,1], p[:,2], M)
                i+=1 

        return M, evecs


