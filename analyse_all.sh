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
#SBATCH --output=analysis.o
#SBATCH --error=analysis.err

source /home/matthew/mambaforge/bin/activate openbiosim
python3 --version

maindir="$PWD"
for filename in ./Systems/*; do
        cd $filename
        echo "System directory = $PWD"
	systemfolder="$PWD"
	for rep in ./rep*; do
		cd $rep/solv
		echo "$PWD"
		cd lambda_0.0000
		python ~/mambaforge/envs/openbiosim/share/Sire/scripts/lj-tailcorrection.py -t somd.prm7 -c somd.rst7 -m somd.pert -C somd.cfg -l 0.00 -r traj000000001.dcd -s 1 1> ../freenrg-LJCOR-lam-0.000.dat 2> /dev/null
		wait
		cd ..
		cd lambda_1.0000
		echo "$(pwd)"
		python ~/mambaforge/envs/openbiosim/share/Sire/scripts/lj-tailcorrection.py -t somd.prm7 -c somd.rst7 -m somd.pert -C somd.cfg -l 1.00 -r traj000000001.dcd -s 1 1> ../freenrg-LJCOR-lam-1.000.dat 2> /dev/null
		cd ..
		wait
		cd $systemfolder
		echo "$PWD"
	done
	cd $maindir$filename
	echo "$PWD"
	python $maindir/analysis.py > hydration_energy.out
	cd $maindir
done
