#!/bin/bash

cd ../
maindir="$PWD"
cd python
rm SMILES.csv
echo "SMILES file_origin mol" >> SMILES.csv
for file in $maindir/ligands/*/; do
	cd $file
	echo "$PWD"
	info=$(obabel -ipdb -ocan solute.pdb)
	cd $maindir/python
	echo "$info $file" >> SMILES.csv
done
