#!/bin/bash

rm SMILES.csv
echo "SMILES file_origin mol" >> SMILES.csv
for file in ./ligands/*/; do
	cd $file
	echo "$PWD"
	info=$(obabel -ipdb -ocan solute.pdb)
	cd ../../
	echo "$info $file" >> SMILES.csv
done
