#Hydration Free Energy
A set of scripts used to reproduce the hydration free energy results of [Leoffler _et al_](10.1021/acs.jctc.8b00544) using BioSimSpace. Currently designed to be run specifically on the Yoko cluster.

##Usage
* First run "run_generate.sh", this will generate smiles strings for all molecules in the "ligands" folder, placing a file named "SMILES.csv" in the "python" folder. It will then generate perturbable systems in both vacuum and solvent, reading the syste>
* A folder named "Systems" will be created, containing all of the pertubable systems - this is where all simulation data will be stored. Currently 3 replicas of each system are generated.
* One system generation is complete, run "MinEqallsystems.sh", this will loop over every perturbable system in "Systems", minimising the vacuum systems, and minimising and equilibrating the solvated systems.
* Once Minimisation and equilibration are complete, run "runallsystems.sh". This will run all vacuum and solvated systems for all replicas (expect this to take a while).
* Once all simulations are complete, run "analyse_all.sh" to analyse all simulations. This will generate a file called "Free_en_outs.out" in each perturbable system folder, as well as adding to the "results.csv" file in the "energy_results" folder.
