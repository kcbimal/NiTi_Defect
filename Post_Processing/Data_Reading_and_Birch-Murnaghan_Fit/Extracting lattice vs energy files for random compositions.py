# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:37:41 2023

@author: Cesar Diaz-Caraveo, Jorge Muñoz
cdiazcarav@miners.utep.edu, cesar.dc1509@gmail.com
jamunoz@utep.edu

The University of Texas at El Paso

Code created as part of the scripts needed for writing the paper 
"Finite-temperature free energies of bcc-based Ni-Ti alloys with thermal and 
chemical disorder from molecular dynamics" 

The program renames and extracts the multiple lattice vs energy files from 
the simulation directories 1 to 5 in the case of the random compositions. 
The multiple excel files created are read as input for the Birch Murnangham 
equation fit by other codes already implemented.

"""

import os 
import shutil
import numpy as np
import pandas as pd

titanium_composition = 0.5
ti_comp = titanium_composition
ni_comp = 1 - titanium_composition
#%%
temp = temperatures
par_dir = "C:\\Users\\biknb\\Downloads\\Cesar\\Spring_2024\\NiTi\\"
file_directory = par_dir + f"MD_Simulations\\MD_Simulations_{temp}K\\Ni{titanium_composition}Ti{1-titanium_composition}\\Ordered_compositions\\"
parent_dir = file_directory
# parent_dir = os.getcwd()

#%%
for i in range(5):
    
    parent_dir_simulation = os.path.join(parent_dir, "Simulation {}".format(i+1))
    os.chdir(parent_dir_simulation)
    
    '''os.rename("Lattice vs Energy Ni{}Ti{} - 500 timesteps.xlsx".format(ni_comp, ti_comp), 
              "Lattice vs Energy Ni{}Ti{} - 500 timesteps - Simulation {}.xlsx".format(ni_comp, ti_comp, i+1))
    os.rename("Lattice vs Energy Ni{}Ti{} - 1000 timesteps.xlsx".format(ni_comp, ti_comp), 
              "Lattice vs Energy Ni{}Ti{} - 1000 timesteps - Simulation {}.xlsx".format(ni_comp, ti_comp, i+1))'''
    
    file_name_copy_500 = "Lattice vs Energy Ni{}Ti{} - 500 timesteps - Simulation {}.xlsx".format(ni_comp, ti_comp, i+1)
    file_name_copy_1000 = "Lattice vs Energy Ni{}Ti{} - 1000 timesteps - Simulation {}.xlsx".format(ni_comp, ti_comp, i+1)
    
    source_dir_copy = os.path.join(parent_dir_simulation, file_name_copy_500)
    dest_dir_copy = os.path.join(parent_dir, file_name_copy_500)
    shutil.copy(source_dir_copy, dest_dir_copy)
    
    source_dir_copy = os.path.join(parent_dir_simulation, file_name_copy_1000)
    dest_dir_copy = os.path.join(parent_dir, file_name_copy_1000)
    shutil.copy(source_dir_copy, dest_dir_copy)
    
    os.chdir(parent_dir)
    