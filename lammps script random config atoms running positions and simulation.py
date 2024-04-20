# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 18:24:21 2021

@authors: Cesar Diaz-Caraveo, Jorge Muñoz
cdiazcarav@miners.utep.edu, cesar.dc1509@gmail.com
jamunoz@utep.edu

The University of Texas at El Paso

Code created as part of the project "Machine Learning the Ground State and Free
Energies of Fe-V Alloys via Cluster Expansions" during the Summer of 
2021, under the mentorship of Prof. Jorge Munoz and funded by the Campus Office
of Undergraduate Research Initiatives.

The code is used for running multiple LAMMPS simulations automatically, 
increasing the lattice parameter each time by a desired amount. It uses the os 
library to send the input files into the terminal, creates a new directory for 
each lattice parameter, and copies the potential and input files to each of 
these new directories. As intial parameters for the simulation, you have the 
titanium composition, and intial lattice parameter value. This code was created 
to find the value of the ground state energy lattice parameter, by getting the 
data of each lattice and finding the minimum on using the "Reading energies 
script for 500 timesteps" and "Reading energies script for 1000 timesteps". 
However, it can be adapted for the user needs. 

Distribution of atoms in the precreated lattice is random in this case, for the 
random composition. titanium composition is specified as parameter at the 
beginning of the code.

"""

import numpy as np
import os
import shutil
import pandas as pd


#%% Location of potential and input files - name input by user
#   Input file must follow the template found in the GitHub repository, and 
#   it needs to be modified depending on the temperature, simulation duration, 
#   and dumping of output values.
temp = temperatures
titanium_composition = 0.5
lattice_value_for = 2.85
par_dir = "C:\\Users\\biknb\\Downloads\\Cesar\\Spring_2024\\NiTi\\"
file_directory = par_dir + f"MD_Simulations\\MD_Simulations_{temp}K\\Ni{1-titanium_compositions}Ti{titanium_compositions}\\Defect_compositions\\sim_steps\\"
# parent_dir = file_directory
# parent_dir = os.getcwd()

#%% Lattice parameters list definition and iteration

lattice_parameters = []

titanium_atoms_unit_cell = int(titanium_composition * 16)

for i in range(40):
    lattice_parameters.append(lattice_value_for)
    lattice_value_for += 0.01
    
#%% Size of the system cell in unit cells assuming a cubic cell, starting at the origin
system_size = 5

#%% Defines total atoms and total titanium atoms
total_atoms = 16 * (system_size ** 3)
total_titanium_atoms = int(titanium_composition * total_atoms)

#%% Defines random positions of titanium atoms in whole atomic configuration
range_total_atoms = np.arange(1, total_atoms + 1)
random_int_array = np.random.choice(range_total_atoms, total_titanium_atoms, 
                                                replace=False)

df_random_numbers = pd.DataFrame(random_int_array)
df_random_numbers.to_csv('Random array for atomic configuration.csv')

#%% Calculates the directory for each lattice parameter, creates the atoms' 
#   positions, and runs the simulations 

for lattice_parameter in lattice_parameters:

    # Unit cell length for NiTi
    unit_cell_length = 2*lattice_parameter
    
    # Defining unit cell
    basis = np.array([[1.0, 0.0, 0.0], 
                      [0.0, 1.0, 0.0],
                      [0.0, 0.0, 1.0]])*unit_cell_length
    
    base_atoms = np.array([[0.0, 0.0, 0.0], 
                           [0.5, 0.0, 0.0],
                           [0.0, 0.5, 0.0], 
                           [0.5, 0.5, 0.0], 
                           [0.0, 0.0, 0.5], 
                           [0.0, 0.5, 0.5], 
                           [0.5, 0.0, 0.5], 
                           [0.5, 0.5, 0.5], 
                           [0.75, 0.25, 0.25], 
                           [0.25, 0.75, 0.25], 
                           [0.25, 0.25, 0.75], 
                           [0.75, 0.75, 0.75], 
                           [0.25, 0.25, 0.25], 
                           [0.75, 0.25, 0.75], 
                           [0.25, 0.75, 0.75], 
                           [0.75, 0.75, 0.25]])*unit_cell_length
    
    # Generate atom positions
    positions = []
    for i in range(system_size):
        for j in range(system_size):
            for k in range(system_size):
                base_position = np.array([i, j, k])
                cart_position = np.inner(basis.T, base_position)
                for atom in base_atoms:
                    positions.append(cart_position + atom)
    
    # Creates subdirectory for the data in source folder 
    sub_directory = 'Simulation_Lattice_{}'.format(round(lattice_parameter, 2))
    parent_dir = os.getcwd()
    
    new_directory = os.path.join(parent_dir, sub_directory)
    os.makedirs(new_directory)
    
    os.chdir(new_directory)
    
    # Copies potentials and input files to each of the directories
    potential_library_dest = os.path.join(new_directory, "NiTi.library.meam")
    shutil.copy(file_directory+"NiTi.library.meam", potential_library_dest)
    
    potential_NiTi_dest = os.path.join(new_directory, "NiTi.meam")
    shutil.copy(file_directory+"NiTi.meam", potential_NiTi_dest)
    
    input_file_dest = os.path.join(new_directory, "NiTi_external_positions_input_file.in")
    shutil.copy(file_directory+"NiTi_external_positions_input_file.in", input_file_dest)
    
    # Sequence of lines to write positions' data in LAMMPS format
    with open('atoms_positions.data', 'w') as fdata:
            #First line included as comment
            fdata.write('Crystalline NiTi atoms - written by EnCodeVentor tutorial\n\n')
            
            #-----Header-----#
            # Specify number of atoms and atom types
            fdata.write('# lattice parameter {} \n \n'.format(round(lattice_parameter, 2)))
            fdata.write('{} atoms\n'.format(total_atoms))
            fdata.write('{} atom types\n'.format(2))
            
            # Specify box dimensions
            fdata.write('{} {} xlo xhi\n'.format(0.0, system_size*unit_cell_length))
            fdata.write('{} {} ylo yhi\n'.format(0.0, system_size*unit_cell_length))
            fdata.write('{} {} zlo zhi\n'.format(0.0, system_size*unit_cell_length))
            fdata.write('\n')
            
            # Atoms section
            fdata.write('Atoms\n\n')
            
            # Write each position as defining it as iron or titanium
            unit_cell_index = 1
            
            for i,pos in enumerate(positions):
                if unit_cell_index in random_int_array:
                    fdata.write('{} 2 {} {} {}\n'.format(i+1, *pos))
                    unit_cell_index += 1
                else:
                    fdata.write('{} 1 {} {} {}\n'.format(i+1, *pos))
                    unit_cell_index += 1
                    
    
    #os.popen("~/lammps-stable_3Mar2020/src/lmp_mpi -in NiTi_external_positions_input_file.in")
    
    os.chdir(parent_dir)
    