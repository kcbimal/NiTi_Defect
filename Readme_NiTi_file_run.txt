>> Structure         : Disordered (finite ordered)
>> Composition Ni-Ti : 50-50 
>> Defect %          : 50 %
>> starting a0 (A^0) : 2.85 (anticipated a0 = 3.01)
>> system size (SS)  : 20
>> nat= 2 *(SS ** 3) : 16000
>> Potential type    : MEAM


>> Files             : *.meam; *.in; lammps script ordered .... .py
>> Simulations       : LAMMPS NVT
                     : temp(K) = 200, 300, 400
                     : timestep = 0.005 = 5fs
                     : run = 2000*0.005 = 5ps
                     : dump every 50
                     : Simulation 1,2,3,4,5 with 39 lattice param for each

>> Post Processing   : Birch-Murnaghan fit 
                       a.: Reading energy script.py (for ts = 500 and 1000 only)
                       b.: EOS Birch-Murnaghan.py (Guess: E0, B0, B0'= -4, 140, 4)
                     
                     : Thermo Calculation
                       a.: Thermodynamic quantities and error calculator.py
                         : manually fill values in "Ni-Ti_defect.csv" from 
                           "Errors and Parameters Birch Murnaghan 0.5.csv"
                           (change header "300K" to designated temperature)
                         :or use code "Reading Birch Murnagham Errors Script - Thermo Code Format.py"


>> Plotting          : 3 plots (2 for energies and 1 for EOS_BM obtained above)

>> Dispersions      :Plot dispersion curve for min. lattice param's only using HELD
                      

           