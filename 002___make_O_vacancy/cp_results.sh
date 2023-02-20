dst='/scratch/x2294a07/SOFC/003___Vacancy_run/BCTZ_rest/result'
for i in BCTZ_*;do
    towards=`echo ${dst}/${i}/defect_cell`
    mkdir -p ${towards}
    cp ${i}/selected_vac/{CONTCAR,OUTCAR,vasprun.xml} ${towards}
    echo ${i} done
done
