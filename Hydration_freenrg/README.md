# Hydration Free Energy
A set of scripts used to reproduce the hydration free energy results of [Leoffler _et al_](10.1021/acs.jctc.8b00544) using BioSimSpace. Currently designed to be run specifically on the Yoko cluster.

## Usage
* First run ``run_generate.sh``, this will generate smiles strings for all molecules in the ``ligands`` folder, placing a file named ``SMILES.csv`` in the ``python`` folder. It will then generate perturbable systems in both vacuum and solvent.
* A folder named ``Systems`` will be created, containing all of the pertubable systems - this is where all simulation data will be stored. Currently 3 replicas of each system are generated.
* One system generation is complete, run ``min_eq_all_systems.sh``, this will loop over every perturbable system in ``Systems``, minimising the vacuum systems, and minimising and equilibrating the solvated systems. All minimisation and equilibration is perfromed using vanilla OpenMM.
* Once Minimisation and equilibration are complete, simulations can be run using either ``SOMD1`` or ``SOMD2``. In order to run simulations using ``SOMD1`` run ``run_all_somd1.sh``. This will run all vacuum and solvated systems for all replicas using the SOMD1 protocol defined in ``mineq_solv.py`` and ``mineq_vac.py`` (expect this to take a while). In order to run simulations with ``SOMD2`` run ``run_all_somd2.sh``, this will run all vacuum and solvated legs using the protol defined in ``run_one_somd2.sh``.
* Once all simulations are complete, run ``analyse_all_somd1.sh`` if SOMD1 was used to run simulations, or ``analyse_all_somd2`` if SOMD2 was used. This will generate a file called ``Free_en_outs.out`` in each perturbable system folder, as well as adding to the ``results.csv`` file in the ``energy_results`` folder.

## Notes
* Ensure that, prior to running scripts, the proper conda environment is listed in all bash scripts (``conda activate <your env name>``).
* Protocols for SOMD1 and SOMD2 are defined differently: to alter SOMD1 protocols the relevant ``mineq_*.py`` script should be altered, to alter SOMD2 protocols, the ``run_one_somd2.sh`` script sohuld be altered.
