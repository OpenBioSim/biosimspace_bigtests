import BioSimSpace as BSS
import argparse
import os

"""Script to Minimise and Equilibrate solvated systems according to the nine step
conservative protocol defined in https://doi.org/10.1063/5.0013849
designed to be run in the respective replica folder
"""
#BSS.verbose(True)
solvated = BSS.IO.readPerturbableSystem(
    top0="pertsave_solv0.prm7",
    coords0="pertsave_solv0.rst7",
    top1="pertsave_solv1.prm7",
    coords1= "pertsave_solv1.rst7",
)
#Need to manually change the device index in each CUDA equilibration to 0
#stops wierd interactions with SLURM 
#(can be done with CUDA_VISIBLE_DEVICES instead but this is easier for large scripts)
substring = "CudaDeviceIndex"

minimise_1 = BSS.Protocol.Minimisation(
    steps=1000, restraint="heavy", force_constant=5.0
)
process_m1 = BSS.Process.OpenMM(solvated, minimise_1, work_dir="Minimise_1")
process_m1.start()
process_m1.wait()
min1 = process_m1.getSystem()
print("First Minimisation Complete")

equil_1 = BSS.Protocol.Equilibration(
    timestep=1 * BSS.Units.Time.femtosecond,
    runtime=15 * BSS.Units.Time.picosecond,
    temperature=300 * BSS.Units.Temperature.kelvin,
    restraint="heavy",
    force_constant=5.0,
    thermostat_time_constant=0.5 * BSS.Units.Time.picosecond,
)
process_e1 = BSS.Process.OpenMM(min1, equil_1, work_dir="Equilibrate_1",platform='CUDA')
cfg1 = process_e1.getConfig()
#This will break if there are more than 1 CudaDeviceIndex variables in the config, but I can't see this happening
i = [cfg1.index(s) for s in cfg1 if substring in s]
cfg1[i[0]] = "properties = {'CudaDeviceIndex': '0'}"
process_e1.setConfig(cfg1)
process_e1.start()
process_e1.wait()
eq1 = process_e1.getSystem()
print("First Equilibration Complete")

minimise_2 = BSS.Protocol.Minimisation(
    steps=1000, restraint="heavy", force_constant=2.0
)
process_m2 = BSS.Process.OpenMM(eq1, minimise_2, work_dir="Minimise_2")
process_m2.start()
process_m2.wait()
min2 = process_m2.getSystem()
print("Second Minimisation Complete")

minimise_3 = BSS.Protocol.Minimisation(
    steps=1000, restraint="heavy", force_constant=0.1
)
process_m3 = BSS.Process.OpenMM(min2, minimise_3, work_dir="Minimise_3")
process_m3.start()
process_m3.wait()
min3 = process_m3.getSystem()
print("Third Minimisation Complete")

minimise_4 = BSS.Protocol.Minimisation(steps=1000)
process_m4 = BSS.Process.OpenMM(min3, minimise_4, work_dir="Minimise_4")
process_m4.start()
process_m4.wait()
min4 = process_m4.getSystem()
print("Forth Minimisation Complete")

equil_2 = BSS.Protocol.Equilibration(
    timestep=1 * BSS.Units.Time.femtosecond,
    runtime=5 * BSS.Units.Time.picosecond,
    temperature=300 * BSS.Units.Temperature.kelvin,
    pressure=1.0 * BSS.Units.Pressure.bar,
    restraint="heavy",
    force_constant=1.0,
    thermostat_time_constant=1 * BSS.Units.Time.picosecond,
)
process_e2 = BSS.Process.OpenMM(min4, equil_2, work_dir="Equilibrate_2",platform='CUDA')
cfg2 = process_e2.getConfig()
i = [cfg2.index(s) for s in cfg2 if substring in s]
cfg2[i[0]] = "properties = {'CudaDeviceIndex': '0'}"
process_e2.setConfig(cfg2)
process_e2.start()
process_e2.wait()
eq2 = process_e2.getSystem()
print("Second Equilibration Complete")

equil_3 = BSS.Protocol.Equilibration(
    timestep=1 * BSS.Units.Time.femtosecond,
    runtime=5 * BSS.Units.Time.picosecond,
    temperature=300 * BSS.Units.Temperature.kelvin,
    pressure=1.0 * BSS.Units.Pressure.bar,
    restraint="heavy",
    force_constant=0.5,
    thermostat_time_constant=1 * BSS.Units.Time.picosecond,
)
process_e3 = BSS.Process.OpenMM(eq2, equil_3, work_dir="Equilibrate_3",platform='CUDA')
cfg3 = process_e3.getConfig()
i = [cfg3.index(s) for s in cfg3 if substring in s]
cfg3[i[0]] = "properties = {'CudaDeviceIndex': '0'}"
process_e3.setConfig(cfg3)
process_e3.start()
process_e3.wait()
eq3 = process_e3.getSystem()
print("Third Equilibration Complete")

equil_4 = BSS.Protocol.Equilibration(
    timestep=1 * BSS.Units.Time.femtosecond,
    runtime=10 * BSS.Units.Time.picosecond,
    temperature=300 * BSS.Units.Temperature.kelvin,
    pressure=1.0 * BSS.Units.Pressure.bar,
#    restraint="backbone", uncomment for systems contraining protein
#    force_constant=0.5,  "                                         "
    thermostat_time_constant=1 * BSS.Units.Time.picosecond,
)
process_e4 = BSS.Process.OpenMM(eq3, equil_4, work_dir="Equilibrate_4",platform='CUDA')
cfg4 = process_e4.getConfig()
i = [cfg4.index(s) for s in cfg4 if substring in s]
cfg4[i[0]] = "properties = {'CudaDeviceIndex': '0'}"
process_e4.setConfig(cfg4)
process_e4.start()
process_e4.wait()
eq4 = process_e4.getSystem()
print("Forth Equilibration Complete")

equil_5 = BSS.Protocol.Equilibration(
    timestep=2 * BSS.Units.Time.femtosecond,
    runtime=10 * BSS.Units.Time.picosecond,
    temperature=300 * BSS.Units.Temperature.kelvin,
    pressure=1.0 * BSS.Units.Pressure.bar,
    thermostat_time_constant=1.0 * BSS.Units.Time.picosecond,
)
process_e5 = BSS.Process.OpenMM(eq4, equil_5, work_dir="Equilibrate_5",platform='CUDA')
cfg5 = process_e5.getConfig()
i = [cfg5.index(s) for s in cfg5 if substring in s]
cfg5[i[0]] = "properties = {'CudaDeviceIndex': '0'}"
process_e5.setConfig(cfg5)
process_e5.start()
process_e5.wait()
eq5 = process_e5.getSystem()
print("Fifth Equilibration Complete")

protocol_run = BSS.Protocol.FreeEnergyProduction(
    num_lam=17,
    runtime=BSS.Types.Time(2.0, "ns"),
    report_interval=10000,
    restart_interval=100,
    temperature=BSS.Types.Temperature(298, "K"),
)

solv_somd = BSS.FreeEnergy.Relative(
    eq5,
    protocol_run,
    engine="somd",
    work_dir="solv",
    extra_options={"minimise": "True","gpu":"0"},
    setup_only=True,
)
print("Success!")

