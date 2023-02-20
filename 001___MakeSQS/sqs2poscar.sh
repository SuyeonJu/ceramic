cell_length=5.41356
for file in composition_*;do
    cd $file
    max_number=`ls  | grep 'bestsqs-' | wc -l`
    ../sqs2poscar bestsqs-${max_number}.out
    mv bestsqs-${max_number}.out-POSCAR _POSCAR
    sed 's/xxx/'${cell_length}'/g' _POSCAR > POSCAR
    echo ${file} done
    cd ..
done
