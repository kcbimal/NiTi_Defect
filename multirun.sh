for f in */ ; 
	do 
	
	cd ${f} ; 
	 mpiexec -np 2 lmp_mpi -in *.in -e screen
	
	cd ../ ; 
done
