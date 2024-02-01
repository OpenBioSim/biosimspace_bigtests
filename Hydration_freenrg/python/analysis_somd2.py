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
import signal, time

class Timeout():
  """Timeout class using ALARM signal"""
  class Timeout(Exception): pass

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    signal.signal(signal.SIGALRM, self.raise_timeout)
    signal.alarm(self.sec)

  def __exit__(self, *args):
    signal.alarm(0) # disable alarm

  def raise_timeout(self, *args):
    raise Timeout.Timeout()

pert_file = os.getcwd()
print(f"LOCAtiON {pert_file}")
list_of_dirs = pert_file.split("/")
pert = list_of_dirs[-1].split("_")

list_of_reps = []
for root, dir, files in os.walk("./"):
    for di in dir:
        if di.startswith("rep"):
            list_of_reps.append(di)

print(list_of_reps)
results_file = os.path.join("../../", "energy_results/results_1fs_nopert.csv")
out = open("Free_en_outs.out", "w")
free_ens = []
errs = []
ens_vac = []
err_vac = []
ens_solv = []
err_solv = []
s_r = 0  # counts the number of successful replicas
for rep in list_of_reps:
    file = os.path.join(rep, "solvated_prod_nopertrest")
    if not os.path.isdir(os.path.join(rep, "solvated_prod_nopertrest")):
        out.write(
            f"{rep} failed due to lack of solv directory ({file})- likely that Min/Eq failed \n"
        )
        continue
    if not os.path.isdir(os.path.join(rep, "vacuum_prod_nopertrest")):
        out.write(
            rep + " failed due to lack of vac directory - likely that Min/Eq failed \n"
        )
        continue
    try:
        with Timeout(60):
            pmf_solv, overlap_solv = BSS.FreeEnergy.Relative.analyse(
                os.path.join("./", rep, "solvated_prod_nopertrest"), estimator="MBAR"
            )
        print(BSS.FreeEnergy.Relative.difference(pmf_solv)[0].value())
        ens_solv.append(BSS.FreeEnergy.Relative.difference(pmf_solv)[0].value())
        err_solv.append(BSS.FreeEnergy.Relative.difference(pmf_solv)[1].value())
    except:
        out.write(
            "\n Free energy analysis failed on "
            + rep
            + " solv, likely that one or more lambda windows crashed"
        )
        continue
    try:
        with Timeout(60):
            pmf_vac, overlap_vac = BSS.FreeEnergy.Relative.analyse(
                os.path.join("./", rep, "vacuum_prod_nopertrest"), estimator="MBAR"
            )
        print(BSS.FreeEnergy.Relative.difference(pmf_vac)[0].value())
        ens_vac.append(BSS.FreeEnergy.Relative.difference(pmf_vac)[0].value())
        err_vac.append(BSS.FreeEnergy.Relative.difference(pmf_vac)[1].value())
    except Exception as e:
        out.write(
            "\n Free energy analysis failed on "
            + rep
            + " vac, likely that one or more lambda windows crashed"
        )
        print(e)
        continue
    free_en = BSS.FreeEnergy.Relative.difference(pmf_solv, pmf_vac)
    free_ens.append(free_en[0].value())
    errs.append(free_en[1].value())
    out.write("\n" + rep)
    out.write(
        "\n Overall Hydration Free Energy for this run = " + str(free_en[0].value())
    )
    s_r += 1
avg = np.nanmean([f for f in free_ens])
err = math.sqrt(np.sum([f**2 for f in errs]))
avg_solv = np.nanmean([f for f in ens_solv])
err_solv = math.sqrt(np.sum([f**2 for f in err_solv]))
avg_vac = np.nanmean([f for f in ens_vac])
err_vac = math.sqrt(np.sum([f**2 for f in err_vac]))
if not np.isnan(avg):
    out.write("\n Average Free Energy = " + str(avg))
if err:
    out.write("\n Error = " + str(err))
out.close()
energies_dict = {}  # Data to append to csv containing energies
# titles = ["mol0","mol1","free_energy","error","successful_reps","date"]
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
if not np.isnan(avg_solv):
    energies_dict["free_energy_solv"] = [avg_solv]
else:
    energies_dict["free_energy_solv"] = [np.nan]
if not np.isnan(err_solv):
    energies_dict["error_solv"] = [err_solv]
else:
    energies_dict["error_solv"] = [np.nan]
if not np.isnan(avg_vac):
    energies_dict["free_energy_vac"] = [avg_vac]
else:
    energies_dict["free_energy_vac"] = [np.nan]
if not np.isnan(err_solv):
    energies_dict["error_vac"] = [err_vac]
else:
    energies_dict["error_vac"] = [np.nan]


energies_dict["successful_reps"] = [s_r]
energies_dict["date"] = [date.today()]
df = pd.DataFrame.from_dict(energies_dict)
df.to_csv(results_file, mode="a", header=False)
