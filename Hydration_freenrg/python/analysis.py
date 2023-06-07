"""Python script designed to find free energies, with error found across multiple runs
Designed to be run in the folder that contains the rep folders (e.g. Systems/Ethane_Methane)"""
import BioSimSpace as BSS
from BioSimSpace._Exceptions import *
import pandas as pd
import os
import numpy as np
import re
import math
from datetime import date

pert_file = os.getcwd()
list_of_dirs = pert_file.split("/")
pert = list_of_dirs[-1].split("_")

list_of_reps = []
for root, dir, files in os.walk("./"):
	for di in dir:
		if di.startswith("rep"):
			list_of_reps.append(di)

results_file = os.path.join("../../","energy_results/results.csv")
out = open("Free_en_outs.out","w")
free_ens = []
errs = []
s_r=0 #counts the number of successful replicas
for rep in list_of_reps:
	if not os.path.isdir(os.path.join(rep,"solv")):
        	out.write(rep + " failed due to lack of solv directory - likely that Min/Eq failed \n")
        	continue
	if not os.path.isdir(os.path.join(rep,"vac")):
		out.write(rep + " failed due to lack of vac directory - likely that Min/Eq failed \n")
		continue
	try:
		pmf_solv, overlap_solv = BSS.FreeEnergy.Relative.analyse(os.path.join("./",rep,"solv"))
	except AnalysisError:
		out.write("\n Free energy analysis failed on " + rep + " solv, likely that one or more lambda windows crashed") 
		continue
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
	try:
		pmf_vac, overlap_vac = BSS.FreeEnergy.Relative.analyse(os.path.join("./",rep,"vac"))
	except AnalysisError:
		out.write("\n Free energy analysis failed on " + rep + " vac, likely that one or more lambda windows crashed")
		continue
	free_en = BSS.FreeEnergy.Relative.difference(pmf_solv,pmf_vac)
	free_ens.append(free_en[0].value()+lj_correction)
	errs.append(free_en[1].value())
	out.write("\n" + rep)
	out.write("\n Base Free Energy = " + str(free_en))
	out.write("\n Lennard-jones Correction = " + str(lj_correction))
	out.write("\n Overall Hydration Free Energy for this run = " + str(free_en[0].value()+lj_correction))
	s_r += 1
avg = np.nanmean([f for f in free_ens])
err = math.sqrt(np.sum([f**2 for f in errs]))
if not np.isnan(avg):
	out.write("\n Average Free Energy = " + str(avg))
if err:
	out.write("\n Error = " + str(err))
out.close()
energies_dict = {} #Data to append to csv containing energies
#titles = ["mol0","mol1","free_energy","error","successful_reps","date"]
energies_dict["mol0"] = [pert[0]]
energies_dict["mol1"] = [pert[1]]
if not np.isnan(avg):
	energies_dict["free_energy"] = [avg]
else:
	energies_dict["free_energy"] = [np.nan]
if not np.isnan(err):
        energies_dict["error"] = [err]
else:
        energies_dict["error"] = [np.nan]
energies_dict["successful_reps"] = [s_r]
energies_dict["date"] = [date.today()]
df=pd.DataFrame.from_dict(energies_dict)
df.to_csv(results_file,mode='a',header=False)
