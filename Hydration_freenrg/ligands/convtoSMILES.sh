#!/bin/bash

rm Inputs.csv
echo "SMILES, file_origin, mol" >> Inputs.csv
for file in ./*/; do
	cd $file
	echo "$file"
	thing=$(obabel -ipdb -ocan solute.pdb)
	cd ..
	echo "$thing, $file" >> Inputs.csv
done
