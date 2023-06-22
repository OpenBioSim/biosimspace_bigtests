#!/bin/bash
#SBATCH -n 1
    # Request 1 gpu per job
#SBATCH --gres=gpu:1
    # allocate 5 processors/CPUs per GPU
#SBATCH --cpus-per-gpu 5
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=genall
#SBATCH --output=./scriptouts/systemgenerate.o
#SBATCH --error=./scriptouts/systemgenerate.err

eval "$(conda shell.bash hook)"
conda activate openbiosim
python3 --version
./convtoSMILES.sh
cd ../
python ./python/generate_systems.py > ./bash_scripts/scriptouts/python_generate.out
wait

