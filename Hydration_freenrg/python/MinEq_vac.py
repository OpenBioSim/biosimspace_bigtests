"""Minimisation of the vacuum systems using the default BioSimSpace minimisation protocol"""
import BioSimSpace as BSS

vac = BSS.IO.readPerturbableSystem(
    top0="pertsave_vac0.prm7",
    coords0="pertsave_vac0.rst7",
    top1="pertsave_vac1.prm7",
    coords1= "pertsave_vac1.rst7",
)

minimise = BSS.Protocol.Minimisation()
process_m1 = BSS.Process.OpenMM(vac, minimise, work_dir="Minimise_Vacuum")
process_m1.start()
process_m1.wait()
min1 = process_m1.getSystem()
print("Minimisation Complete")

protocol_run = BSS.Protocol.FreeEnergyProduction(
    num_lam=17,
    runtime=BSS.Types.Time(2.0, "ns"),
    report_interval=10000,
    restart_interval=100,
    temperature=BSS.Types.Temperature(298, "K"),
)

vac_somd = BSS.FreeEnergy.Relative(
    min1,
    protocol_run,
    engine="somd",
    work_dir="vac",
    extra_options={"minimise": "True","gpu":"0"},
    setup_only=True,
)
print("Success!")

