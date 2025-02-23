#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# My first example with AutoDock Vina in python
#
import os
import subprocess
import timeout_decorator
from vina import Vina


v = Vina(sf_name='vina', cpu = 6, seed = 12345)

# v.set_receptor('/Users/yashravipati/Downloads/PDBBind_processed/1a4g/1a4g_protein_processed.pdb.pdbqt')

# v.set_ligand_from_file('/Users/yashravipati/Downloads/PDBBind_processed/1a4g/1a4g_ligand.mol2.pdbqt')
# v.compute_vina_maps(center=[15.190, 53.903, 16.917], box_size=[20, 20, 20])

@timeout_decorator.timeout(5)
def dock_vina(receptor_file, ligand_file):
    v.set_receptor(receptor_file)
    v.set_ligand_from_file(ligand_file)
    v.compute_vina_maps(center=[15.190, 53.903, 16.917], box_size=[20, 20, 20])
    v.dock(exhaustiveness=32, n_poses=20)
    v.write_poses(ligand_file[:-5] + "_docked.pdbqt", n_poses=5, overwrite=True)

root_dir = "/Users/yashravipati/Downloads/PDBBind_processed"

x = 0
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".pdbqt"):
            # Check if the file is a receptor or a ligand
            if "protein" in filename:
                receptor_file = os.path.join(dirpath, filename)
                x += 1
            elif "ligand" in filename:
                ligand_file = os.path.join(dirpath, filename)
                x += 1
                # Dock the receptor and ligand
            if x == 2:
                print(receptor_file + "\n" + ligand_file) 
                x=0
                try:
                    dock_vina(receptor_file, ligand_file)
                except timeout_decorator.timeout_decorator.TimeoutError:
                    print("Skipping iteration as it took too long")
                    continue  # move on to the next iteration
