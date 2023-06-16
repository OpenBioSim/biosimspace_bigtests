#!/bin/bash
#SBATCH -n 1
    # Request 1 gpu per job
#SBATCH --gres=gpu:1
    # allocate 5 processors/CPUs per GPU
#SBATCH --cpus-per-gpu 5
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=solv_run
#SBATCH --output=solv.%j.o
#SBATCH --error=solv.%j.er

eval "$(conda shell.bash hook)"
conda activate openbiosim
python3 --version

lamvals=( 0.0000 0.0625 0.1250 0.1875 0.2500 0.3125 0.3750 0.4375 0.5000 0.5625 0.6250 0.6875 0.7500 0.8125 0.8750 0.9375 1.0000 )
lam=${lamvals[SLURM_ARRAY_TASK_ID]}

echo "lambda is: " $lam

cd ./solv/lambda_$lam
echo "$PWD"
srun somd-freenrg -C ./somd.cfg -c ./somd.rst7 -t ./somd.prm7 -m ./somd.pert -p CUDA -l $lam
cd ..
wait
