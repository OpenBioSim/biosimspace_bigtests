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
cd ../
sdir="$PWD"
for filename in ./Systems/*; do
	cd $filename
	echo "before running $PWD"
	cd ../../
	echo "after runnning $PWD"
done
