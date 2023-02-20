dir_path='Doped_Ce'
batch_file='/scratch/x2294a07/SOFC/003___Vacancy_run/batch_nurion.j'
cd ${dir_path}

for i in Doped_Ce_*;do
    sed 's/JOBTITLE/'$i'_Vac/g' ${batch_file} > $i/selected_vac/batch.j
    cd $i/selected_vac
# mv CONTCAR POSCAR
    qsub batch.j
    cd ../../
done
