#!/bin/bash
#SBATCH -n 1
    # Request 1 gpu per job
#SBATCH --gres=gpu:1
    # allocate 5 processors/CPUs per GPU
#SBATCH --cpus-per-gpu 5
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=runall
#SBATCH --output=./scriptouts/runall.o
#SBATCH --error=./scriptouts/runall.err

source /home/matthew/mambaforge/bin/activate openbiosim
python3 --version
cd ../
maindir="$PWD"
for filename in ./Systems/*; do
	cd $filename
	echo "System directory = $PWD"
	for rep in ./rep*; do
		cd $rep
		echo "rep directory = $PWD"
		sbatch --wait --array=0-16 $maindir/bash_scripts/runonesystem_solv.sh
		sbatch --wait --array=0-16 $maindir/bash_scripts/runonesystem_vac.sh
		cd ..
	done
	cd $maindir
done
