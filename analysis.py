"""Python script designed to find free energies, with error found across multiple runs
Designed to be run in the folder that contains the rep folders (e.g. Systems/Ethane_Methane)"""
import BioSimSpace as BSS
import pandas as pd
import os
import numpy as np
import re
import math

list_of_reps = []
for root, dir, files in os.walk("./"):
	for di in dir:
		if di.startswith("rep"):
			list_of_reps.append(di)

out = open("Free_en_outs.out","w")
free_ens = []
errs = []
for rep in list_of_reps:
	pmf_solv, overlap_solv = BSS.FreeEnergy.Relative.analyse(os.path.join("./",rep,"solv"))
	print(os.path.join("./",rep,"solv"))
	files = [os.path.join("./",rep,"solv","freenrg-LJCOR-lam-0.000.dat"),os.path.join("./",rep,"solv","freenrg-LJCOR-lam-1.000.dat")]
	print(os.path.join("./",rep,"solv","freenrg-LJCOR-lam-0.000.dat"))
	corrs = []
	#gets the energies in order [0,1], needs to output 1-0
	for file in files:
		print(file)
		with open(file,"r") as f:
			lines = f.read().splitlines()
			last_line = lines[-1]
			ll = last_line
			ls = re.findall(r"[-+]?(?:\d*\.*\d+)",ll)
			corrs.append(float(ls[0]))
	lj_correction=corrs[1]-corrs[0]
	pmf_vac, overlap_vac = BSS.FreeEnergy.Relative.analyse(os.path.join("./",rep,"vac"))
	free_en = BSS.FreeEnergy.Relative.difference(pmf_solv,pmf_vac)
	free_ens.append(free_en[0].value()+lj_correction)
	errs.append(free_en[1].value())
	out.write("\n" + rep)
	out.write("\n Base Free Energy = " + str(free_en))
	out.write("\n Lennard-jones Correction = " + str(lj_correction))
	out.write("\n Overall Hydration Free Energy for this run = " + str(free_en[0].value()+lj_correction))
avg = np.average([f for f in free_ens])
err = math.sqrt(np.sum([f**2 for f in errs]))
out.write("\n Average Free Energy = " + str(avg))
out.write("\n Error = " + str(err))
out.close()
