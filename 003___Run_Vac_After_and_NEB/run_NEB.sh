for i in BSCF*;do
    cd $i
    sed 's/JOBTITLE/NEB_'${i}'/g' batch_NEB.j > batch_NEB_new.j
    cp batch_NEB_new.j O*/batch_NEB.j
    cp INCAR_NEB O*/INCAR
    cd O*
    for j in {01..03};do
        cp INCAR $j
    done
    qsub batch_NEB.j
    cd ../../
done
