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
#SBATCH --output=./scriptouts/MinEq.o
#SBATCH --error=./scriptouts/MinEq.err

eval "$(conda shell.bash hook)"
conda activate openbiosim
python --version
cd ../
sdir="$PWD"
reps=( rep1 rep2 rep3 )
for filename in ./Systems/*; do
	cd $filename
	echo "$PWD"
	sbatch --array=0-2 $sdir/bash_scripts/MinEqonesystem.sh
	cd ../../
done
#Generates an extremely simple report that records success or failure of each simulation
#python ./python/MinEq_report.py now defunct
