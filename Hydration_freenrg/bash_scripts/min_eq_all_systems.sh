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
#Write a yaml file containing environment information in to the environments folder
conda env export > $sdir/environments/$(date +"%Y-%d-%m").yml
for filename in ./Systems/*; do
	cd $filename
	echo "$PWD"
	sbatch --array=0-2 $sdir/bash_scripts/min_eq_one_system.sh
	cd ../../
done
