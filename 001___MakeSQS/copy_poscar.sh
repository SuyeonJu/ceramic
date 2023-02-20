for i in composition_*;do
    poscar_no=`echo ${i} | sed 's/composition_//g'`
    cp $i/POSCAR ./POSCAR_CSTZ_o_${poscar_no}
done
