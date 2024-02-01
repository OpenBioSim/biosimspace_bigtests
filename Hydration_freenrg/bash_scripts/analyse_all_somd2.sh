#!/bin/bash
#SBATCH -n 1
#SBATCH --cpus-per-task 4
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=analysis
#SBATCH --output=./scriptouts/analysis.o
#SBATCH --error=./scriptouts/analysis.err

export CUDA_VISIBLE_DEVICES=""
eval "$(conda shell.bash hook)"
conda activate sireDEV
python3 --version
cd ../
maindir="$PWD"
echo "master dir is $maindir"
for filename in "$maindir"/Systems/*; do
        cd $filename
        echo "System directory = $PWD"
	systemfolder="$PWD"
	cd $maindir$filename
	echo "HERE $PWD"
	python $maindir/python/analysis.py > hydration_energy.out
	cd $maindir
done

