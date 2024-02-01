"""Minimisation of the vacuum systems using the default BioSimSpace minimisation protocol"""
import BioSimSpace as BSS


class MinimisationError(Exception):
    """Exception raised when failure occured during a minimisation step

    Attributes:
        min -- minimisation step that caused failure
        message -- explanation of error
    """

    def __init__(self, min, message="Minimisation Failed"):
        self.min = min
        self.message = message
        super().__init__(self.message)


class GetSystemError(Exception):
    """Exception raised when a system of value None is found

    Attributes:
        sys -- name of none system
        message -- explanation of error
    """

    def __init__(self, sys, message="System with value None found"):
        self.sys = sys
        self.message = message
        super().__init__(self.message)


vac = BSS.IO.readPerturbableSystem(
    top0="pertsave_vac0.prm7",
    coords0="pertsave_vac0.rst7",
    top1="pertsave_vac1.prm7",
    coords1="pertsave_vac1.rst7",
)

minimise = BSS.Protocol.Minimisation()
process_m1 = BSS.Process.OpenMM(vac, minimise, work_dir="Minimise_Vacuum")
process_m1.start()
process_m1.wait()
if process_m1.isError():
    raise MinimisationError(process_m1)
min1 = process_m1.getSystem()
if min1 is None:
    raise GetSystemError(min1)
print("Minimisation Complete")
# Saving binary for somd2
min1.save("mineq_vac")
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
    work_dir="vacuum_somd1",
    extra_options={"minimise": "True", "gpu": "0"},
    setup_only=True,
)
print("Success!")
