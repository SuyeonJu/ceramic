script_path='/scratch/x2294a07/SOFC/001___migration_Run/vacancy_after_NEB.py'
for i in Doped_Ce_*;do
    cd $i
    python ${script_path} POSCAR_perfect_cell POSCAR_defect_cell

    relax_folder=`ls | grep ^O`
    cd ${relax_folder}/relax_after

#    mv POSCAR POSCAR_0000
#    mv OUTCAR OUTCAR_0000
#    mv XDATCAR XDATCAR_0000
#    mv stdout.x std_0000
#    cp CONTCAR POSCAR

#    sed '/walltime/s/24/48/g' ../../batch.j > batch.j

    mv INCAR INCAR_original
    sed '/EDIFFG/s/0.02/0.05/g' INCAR_original > INCAR

#    qsub batch.j

    cd ../../

    cd ..
done
