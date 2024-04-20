for f in */ ; 
	do 
	
	cd ${f} ; 
	 mpiexec -np 2 lmp_mpi -in FeV_external_positions_input_file.in -e screen
	
	cd ../ ; 
done
