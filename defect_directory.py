# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 09:51:08 2024

@author: biknb
"""

import os
import shutil

#%%
def create_directory(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            # print(f"Directory '{path}' created successfully.")
        except FileExistsError:
            print(f"Error: Directory '{path}' could not be created.")
    else:
        print(f"Directory '{path}' already exists.")

def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        # print(f"File '{source}' copied to '{destination}' successfully.")
    except FileNotFoundError:
        print(f"Error: File '{source}' not found.")

def replace_text_in_file(file_path, old_text, new_text):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        
        file_content = file_content.replace(old_text, new_text)
        
        with open(file_path, 'w') as file:
            file.write(file_content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
 
#%%
if __name__ == "__main__":
    
    temperatures = [200, 300, 400]  # You can add more temperature values if needed
    compositions = [0.5]  # Different composition values (Ni0.5Ti0.5)
    sys_size = 20
    def_per = 50

#%%    
    for Temp in temperatures:
        for composition in compositions:
            par_dir = "C:\\Users\\biknb\\Downloads\\Cesar\\Spring_2024\\NiTi\\"
            main_dir = "MDD_Simulations"     #MDD = molecular dynamics defect
            create_directory(main_dir)
    
            # Create subdirectories
            temp_dir = os.path.join(main_dir, f"MDD_simulations_{Temp}K")
            comp_dir = os.path.join(temp_dir, f"Ni{composition}Ti{1-composition}")
            defect_dir = os.path.join(comp_dir, "Defect_compositions")
            sub_dirs = [temp_dir, comp_dir, defect_dir]
            for i in range(1, 6):
                sub_dirs.append(os.path.join(defect_dir, f"Simulation {i}"))

            for dir_path in sub_dirs:
                create_directory(dir_path)
                
#%%            
            # Copy files for Defect
            # defect_files = ["NiTi.library.meam", "NiTi.meam", "NiTi_external_positions_input_file.in", "lammps script ordered simulation - finite order defects.py", "multirun.sh"]
            defect_files = ["NiTi.library.meam", "NiTi.meam", "multirun.sh", "NiTi_external_positions_input_file.in", "lammps script ordered simulation - finite order defects.py"]
            for i in range(1, 6):
                for file in defect_files:
                    source = os.path.join(par_dir, file)
                    if os.path.exists(source):
                        destination = os.path.join(defect_dir, f"Simulation {i}", file)
                        copy_file(source, destination)
                        if file == "lammps script ordered simulation - finite order defects.py":
                            replace_text_in_file(destination, "temperatures", str(Temp))
                            replace_text_in_file(destination, "sys_size", str(sys_size))
                            replace_text_in_file(destination, "def_per", str(def_per))
                            replace_text_in_file(destination, "sim_steps", f"Simulation {i}")
                        elif file == "NiTi_external_positions_input_file.in":
                            replace_text_in_file(destination, "temperatures", str(Temp))
                    else:
                        print(f"Error: File '{file}' not found in '{par_dir}'.")
#%%