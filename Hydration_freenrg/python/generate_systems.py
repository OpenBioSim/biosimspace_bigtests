"""Generates pertubable systems by reading in SMILES for each molecule,
parameterising and then mapping.
Designed to be run from withinthe main directory (Hydration_freenrg)."""

import BioSimSpace as BSS
from BioSimSpace._Exceptions import *
import pandas as pd
import argparse
import os


def try_to_param(name, SMILES):
    print("Parameterising", name, "with SMILES string", SMILES)
    try:
        mol = BSS.Parameters.gaff(SMILES).getMolecule()
    except ParameterisationError:
        print("First attempt failed...trying again with zero net charge")
        try:
            mol = BSS.Parameters.gaff(SMILES, net_charge=0).getMolecule()
        except ParameterisationError:
            print("Zero Net Charge failed...skipping this perturbation")
            mol = 0
    finally:
        return mol


parser = argparse.ArgumentParser(
    prog="generateinputs",
    description="A script to generate inputs for testing BioSimSpace",
)

parser.add_argument(
    "-w",
    "--writedet",
    help="Optional Argument, whether or not to write detailed output, 1 for true, 0 for false",
    type=int,
    default=1,
)

args = parser.parse_args()
# Read in smiles strings for each listed molecule, and parameterise
# Each Molecule then stored in a dictionary by name in order to prevent parameterising the same one multiple times
SMILES = pd.read_csv(os.path.join("./python","SMILES.csv"), delim_whitespace=True)
SMILES["mol"] = [mol.split("/")[-2] for mol in SMILES["mol"]]
molecules = {}
for count, row in SMILES.iterrows():
    name_mol = row["mol"]
    molecules[name_mol.lower()] = try_to_param(name_mol, row["SMILES"])

numreps = 3
perturbations = pd.read_csv("Input_namesonly.csv")
for count, row in perturbations.iterrows():
    name_mol0 = row.Lambda_0
    name_mol1 = row.Lambda_1
    print("Attempting to create perturbable system for", name_mol0, "<-->", name_mol1)
    try:
        mol0 = molecules[name_mol0.lower()]
    except KeyError:
        print(
            "Molecule  "
            + name_mol0
            + " not in parameterised list. Check spelling or add to ligands."
        )
    try:
        mol1 = molecules[name_mol1.lower()]
    except KeyError:
        print(
            "Molecule  "
            + name_mol1
            + " not in parameterised list. Check spelling or add to ligands."
        )
    if not mol0 or not mol1:
        continue
    bigfolder = "Systems"
    if not os.path.exists(bigfolder):
        os.makedirs(bigfolder)
    foldername = os.path.join(bigfolder, name_mol0 + "_" + name_mol1)
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    mapping = BSS.Align.matchAtoms(mol0, mol1)
    # If the writedet option is on, write atom mapping to file
    if args.writedet:
        outfile = "mappings.csv"  # csv chosen so that output file is human readable
    info_mol0 = []
    info_mol1 = []
    mol0atoms = mol0.getAtoms()
    mol1atoms = mol1.getAtoms()
    for idx0, idx1 in mapping.items():
        info_mol0.append(
            [
                mol0atoms[idx0].name(),
                mol0atoms[idx0].moleculeNumber(),
                mol0atoms[idx0].index(),
                mol0atoms[idx0].element().split(" ")[0],
            ]
        )
        info_mol1.append(
            [
                mol1atoms[idx1].name(),
                mol1atoms[idx1].moleculeNumber(),
                mol1atoms[idx1].index(),
                mol1atoms[idx1].element().split(" ")[0],
            ]
        )
    mol0_inv = list(map(list, zip(*info_mol0)))
    mol1_inv = list(map(list, zip(*info_mol1)))
    df = pd.DataFrame(
        {
            "mol0_name": mol0_inv[0],
            "mol0_molnum": mol0_inv[1],
            "mol0_index": mol0_inv[2],
            "mol0_atomname": mol0_inv[3],
            "mol1_name": mol1_inv[0],
            "mol1_molnum": mol1_inv[1],
            "mol1_index": mol1_inv[2],
            "mol1_atomname": mol1_inv[3],
        }
    )
    df.to_csv(os.path.join(foldername, outfile))
    mol0 = BSS.Align.rmsdAlign(mol0, mol1, mapping)
    try:
        merged = BSS.Align.merge(mol0, mol1, mapping)
    except IncompatibleError:
        print("Initial merge failed, trying again with ring size change")
        try:
            merged = BSS.Align.merge(
                mol0,
                mol1,
                mapping,
                allow_ring_size_change=True,
                allow_ring_breaking=True,
            )
        except IncompatibleError as e:
            print(
                "Ring size change and ring breaking failed... skipping this perturbation"
            )
            print(str(e))
            continue
    solvated = BSS.Solvent.tip3p(
        molecule=merged, box=3 * [3 * BSS.Units.Length.nanometer]
    )
    if not os.path.exists(os.path.join(foldername,"slurmouts")):
        os.makedirs(os.path.join(foldername,"slurmouts"))
    for i in range(numreps):
        repfile = os.path.join(foldername, "rep" + str(i))
        BSS.IO.savePerturbableSystem(os.path.join(repfile, "pertsave_solv"), solvated)
        BSS.IO.savePerturbableSystem(
            os.path.join(repfile, "pertsave_vac"), merged.toSystem()
        )
    print("Perturbable System created")
