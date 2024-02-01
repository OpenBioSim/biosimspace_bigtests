#!/bin/bash
#SBATCH -n 1
    # Request 1 gpu per job
#SBATCH --gres=gpu:1
    # allocate 5 processors/CPUs per GPU
#SBATCH --cpus-per-gpu 5
    # allocate 5 GB of memory per job
#SBATCH --mem 5000
    # Set job name
#SBATCH --job-name=analysis
#SBATCH --output=./scriptouts/analysis.o
#SBATCH --error=./scriptouts/analysis.err

eval "$(conda shell.bash hook)"
conda activate openbiosim
python3 --version
cd ../
maindir="$PWD"
echo "master dir is $maindir"
for filename in ./Systems/*; do
        cd $filename
        echo "System directory = $PWD"
	systemfolder="$PWD"
	for rep in ./rep*; do
		cd $rep/solvated_somd1
		echo "$PWD"
		cd lambda_0.0000
		lj-tailcorrection -t somd.prm7 -c somd.rst7 -m somd.pert -C somd.cfg -l 0.00 -r traj000000001.dcd -s 1 1> ../freenrg-LJCOR-lam-0.000.dat 2> /dev/null
		wait
		cd ..
		cd lambda_1.0000
		echo "$(pwd)"
		lj-tailcorrection -t somd.prm7 -c somd.rst7 -m somd.pert -C somd.cfg -l 1.00 -r traj000000001.dcd -s 1 1> ../freenrg-LJCOR-lam-1.000.dat 2> /dev/null
		cd ..
		wait
		cd $systemfolder
		echo "$PWD"
	done
	cd $maindir$filename
	echo "HERE $PWD"
	python $maindir/python/analysis_somd1.py > hydration_energy.out
	cd $maindir
done
