#!/bin/bash
#SBATCH -n 1
    # Request 1 gpu per job
#SBATCH --gres=gpu:1
    # allocate 5 processors/CPUs per GPU
#SBATCH --cpus-per-gpu 5
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=MinEQ
#SBATCH --output=MinEq.o
#SBATCH --error=MinEq.err

source /home/matthew/mambaforge/bin/activate openbiosim
python --version
reps=( rep1 rep2 rep3 )
for filename in ./Systems/*; do
	cd $filename
	echo "$PWD"
	sbatch --array=0-2 ../../MinEqonesystem.sh
	cd ../../
done
#Generates an extremely simple report that records success or failure of each simulation
python MinEq_report.py 
