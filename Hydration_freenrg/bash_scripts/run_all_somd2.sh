#!/bin/bash
#SBATCH -n 1
    # allocate 1 processor as a manager
#SBATCH --cpus-per-task 1
    # allocate 0.1 GB of memory per job
#SBATCH --mem 100
    # Set job name
#SBATCH --job-name=runall
#SBATCH --output=./scriptouts/runall_1fs.o
#SBATCH --error=./scriptouts/runall_1fs.err

eval "$(conda shell.bash hook)"
conda activate sireDEV
python3 --version
cd ../
maindir="$PWD"
for filename in ./Systems/*; do
        cd $filename
        echo "System directory = $PWD"
        for rep in ./rep*; do
                cd $rep
                echo "rep directory = $PWD"
                sbatch --wait $maindir/bash_scripts/run_one_somd2.sh
                cd ..
        done
        cd $maindir
done

