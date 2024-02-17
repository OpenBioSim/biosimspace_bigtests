#!/bin/bash
#SBATCH -n 1
    # Request 1 gpu per job
#SBATCH --gres=gpu:1
    # allocate 5 processors/CPUs per GPU
#SBATCH --cpus-per-gpu 5
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=MinEq
#SBATCH --output=./slurmouts/MinEq.%j.o
#SBATCH --error=./slurmouts/MinEq.%j.err

#Designed to be run from within the /Systems/{currentsystem} folder
#Directory work should be handled by MinEqallsystems.sh
eval "$(conda shell.bash hook)"
conda activate sireDEV
python3 --version
reps=( rep0 rep1 rep2 )
rep=${reps[SLURM_ARRAY_TASK_ID]}
cd $rep
echo "$PWD"
python ../../../python/min_eq_solv.py > solv_mineq_$rep.o
echo "Solvated System Complete"
python ../../../python/min_eq_vac.py > vac_mineq_$rep.o
echo "Vacuum System Complete"
wait
cd ..

