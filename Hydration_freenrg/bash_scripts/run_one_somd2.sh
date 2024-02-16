#!/bin/bash
#SBATCH -n 1
    # Request 1 gpu per job
#SBATCH --gres=gpu:4
    # allocate 5 processors/CPUs per GPU
#SBATCH --cpus-per-gpu 4
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=solv_run
#SBATCH --output=run.%j.o
#SBATCH --error=run.%j.er

eval "$(conda shell.bash hook)"
conda activate sireDEV
python3 --version
file_name_solv="mineq_solv.bss"
file_name_vac="mineq_vac.bss"
# Solvated leg
somd2 ${file_name_solv} --runtime 500ps --timestep 1fs --h-mass-factor 1.0 --num-lambda 17 --temperature 298K --pressure 1atm --checkpoint-frequency 200ns --energy-frequency 0.25ps --output-directory solvated_somd2 --no-restart --cutoff-type rf --cutoff 10.0A --overwrite --perturbable-constraint none --constraint none --somd1-compatibility
wait
#Vacuum leg
somd2 ${file_name_vac} --runtime 500ps --timestep 1fs --h-mass-factor 1.0 --num-lambda 17 --temperature 298K --checkpoint-frequency 1ns --output-directory vacuum_somd2 --energy-frequency 0.25ps --no-restart --cutoff-type rf --cutoff 10.0A --overwrite --perturbable-constraint none --constraint none --somd1-compatibility
wait
