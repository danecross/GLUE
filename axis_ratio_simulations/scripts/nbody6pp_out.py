# functions to process outputs from NBODY6++GPU
# last modified Oct 21, 2020, Vaclav Pavlik, IU

import numpy as np
import struct
import sys
import os.path

def read_conf3(filename, rdens=True, rdens_out=False, henon=True, par_out=False, neigh_out=False, phi_out=False):
	''' Reads 'conf.3_' from NBODY6++GPU. Note that instead of all time blocks in one file (as in NBODY6), each time block has its own file.
	
	Definitions:
	integer NTOT, MODEL, NRUN, NK, NAME(NMAX)
	real*4 AS(20), BODYS(NMAX), RHOS(NMAX), XNS(NMAX),
				 XS(3,NMAX), VS(3,NMAX), PHI(NMAX)
	
	Byte content of 'conf.3_' file:
	write NTOT, MODEL, NRUN, NK
	write (AS(K),K=1,NK), (BODYS(J),J=1,NTOT),
				(RHOS(J),J=1,NTOT),(XNS(J),J=1,NTOT),
				((XS(K,J),K=1,3),J=1,NTOT), ((VS(K,J),K=1,3),J=1,NTOT),
				(PHI(J),J=1,NTOT),(NAME(J),J=1,NTOT)
	
	Parameters
	----------
	filename : string
		Path and name of the OUT3 file.
	rdens : boolean, optional
		If 'True', will return the positions wrt the density centre. If 'False', will return positions in the initial coordinate system. Default 'True'.
	rdens_out : boolean, optional
		If 'True', will return also an array with RDENS coordinates. Default 'False'.
	henon : boolean, optional
		If 'True', give output in Hénon units, i.e. G=M=Rv=-4E=1. If 'False' give output in astrophysical units. Default 'True'.
	par_out : boolean, optional
		If 'True', will return parameters from AS() array. Default 'False'.
	neigh_out : boolean, optional
		If 'True', will return parameters of the neighbors. Default 'False'.
	phi_out : boolean, optional
		If 'True', will return the local potential. Default 'False'.
	
	Returns
	-------
	time : float
		Timestamp of the output file.
	ids : 1-d ndarray
		Indices of stars. Elements: [id]
	mass : 1-d ndarray
		Masses of stars. Elements: [mass]
	pos : 2-d ndarray
		x,y,z coordinates. Elements: [n,xyz]
	vel : 2-d ndarray
		vx,vy,vz coordinates. Elements: [n,xyz]
	rd : 1-d ndarray, optional
		RDENS coordinates. Only if `rdens_out` is 'True'. Elements: [xyz]
	par : 1-d ndarray, only if `par_out` is 'True'.
		Header parametres (TTOT, NPAIRS, RBAR, ZMBAR, RTIDE, TIDAL(4), RDENS(1), RDENS(2), RDENS(3), TTOT/TCR0, TSCALE, VSTAR, RC, NC, VC, RHOM, CMAX, RSCALE, RSMIN, DMIN1). Elements: [par]
	xns : 1-d ndarray, optional
		The fifth nearest neighbor distance, (only avaiable for particles inside core radius). Only if `neigh_out` is 'True'. Elements: [distance]
	rhos : 1-d ndarray, optional
		Mass density of individual star calculated by nearest 5 neighbors (only avaiable for particles inside core radius). Only if `neigh_out` is 'True'. Elements: [rho]
	phi : 1-d ndarray, optional
		Local potential (just from stars, no tidal field). Only if `phi_out` is 'True'. Elements: [xyz]
	'''
	if not os.path.exists(filename):
		raise RuntimeError("No conf.3_ to process. Path to", filename, "does not exist.")
	
	data = open(filename, "rb").read()
	
	# initialize arrays (in nbody6)
	#ids, mass, pos, vel = [], [], [], [], []
	#rd = []
	
	
	# WARNING: Do not forget to remove padding of 4 bytes at the beginning/end of each "write" statement!
	pad = 4

	# unpack `data` to variables
	f = 0
	
	
	''' Read the data. '''
	
	# try to read the next block, i.e. padding at the beginning, or exit
	i, f = f, f + pad
	try:
		struct.unpack(str(pad)+"x", data[i:f])
	except:
		raise RuntimeError("Unknown format of", filename)
	
	i, f = f, f + 4*4
	(NTOT, MODEL, NRUN, NK) = struct.unpack("4i", data[i:f])
	
	# remove padding: 4 bytes at the end & 4 bytes at the beginning
	i, f = f, f + 2*pad
	struct.unpack(str(2*pad)+"x", data[i:f])
	
	# read the block parameters in AS()
	i, f = f, f + NK*4
	AS = struct.unpack(str(NK)+"f", data[i:f])
	
	# few parameters from AS[]
	TTOT = float(AS[0])
	NPAIRS = int(AS[1])
	RBAR = AS[2]
	ZMBAR = AS[3]
	RDENS = np.array([AS[6], AS[7], AS[8]])
	TSCALE = AS[10]
	VSTAR = AS[11]
	
	if henon is False:
		TTOT = TTOT * TSCALE
	
	# read stars
	i, f = f, f + NTOT*4
	BODYS = struct.unpack(str(NTOT)+"f", data[i:f])
	
	i, f = f, f + NTOT*4
	RHOS = struct.unpack(str(NTOT)+"f", data[i:f])
	
	i, f = f, f + NTOT*4
	XNS = struct.unpack(str(NTOT)+"f", data[i:f])
	
	i, f = f, f + 3*NTOT*4
	XS = struct.unpack(str(3*NTOT)+"f", data[i:f])
	
	i, f = f, f + 3*NTOT*4
	VS = struct.unpack(str(3*NTOT)+"f", data[i:f])
	
	i, f = f, f + NTOT*4
	PHI = struct.unpack(str(NTOT)+"f", data[i:f])
	
	i, f = f, f + NTOT*4
	NAME = struct.unpack(str(NTOT)+"i", data[i:f])
	
	# remove padding: 4 bytes at the end
	i, f = f, f + pad
	try:
		struct.unpack(str(pad)+"x", data[i:f])
	except:
		print("Warning:", TTOT, "no end of block.", file=sys.stderr)
	
	# let me know where did you end reading
	#print("End:", TTOT, file=sys.stderr)
	
	''' Process the data. '''
	
	# time
	time = TTOT
	
	# number of stars, pairs
	NSTAR = NTOT - NPAIRS
				
	# positions & velocities
	pos = np.reshape(XS, [NTOT,3], order="A")
	if rdens is True:
		pos = pos[:NSTAR,:] - RDENS
	else:
		pos = pos[:NSTAR,:]
	
	vel = np.reshape(VS, [NTOT,3], order="A")
	vel = vel[:NSTAR,:]
	
	# IDs & masses
	ids = np.array(NAME[:NSTAR])
	mass = np.array(BODYS[:NSTAR])
	
	# other arrays
	if rdens_out is True:
		rd = np.array(RDENS)
	if par_out is True:
		par = np.array(AS)
	if neigh_out is True:
		xns = np.array(XNS[:NSTAR])
		rhos = np.array(RHOS[:NSTAR])
	if phi_out is True:
		phi = np.array(PHI[:NSTAR])
	
	# real astrophysical units
	if henon is False:
		pos = pos * RBAR
		mass = mass * ZMBAR
		vel = vel * VSTAR
		if rdens_out is True:
			rd = rd * RBAR
		if neigh_out is True:
			xns = xns * RBAR
			rhos = rhos * ZMBAR / RBAR**3
		if phi_out is True:
			phi = phi * ZMBAR * RBAR**2 / TSCALE**2
	
	# return
	ret = time, ids, mass, pos, vel
	if rdens_out is True: ret = ret + (rd,)
	if par_out is True: ret = ret + (par,)
	if neigh_out is True:  ret = ret + (xns,) + (rhos,)
	if phi_out is True:  ret = ret + (phi,)
	
	return ret

