# Make INCAR file for each folder

# Need INCAR, POSCAR in the working directory
dir_path='Doped_Ce'

for i in ${dir_path}/*;do
    # get the number of each atom type
    atom_info=`awk 'NR == 7 {print $0}' ${i}/POSCAR`
    natom_1=`echo ${atom_info} | awk '{print $1}'`
    natom_2=`echo ${atom_info} | awk '{print $2}'`
    natom_3=`echo ${atom_info} | awk '{print $3}'`
    natom_4=`echo ${atom_info} | awk '{print $4}'`
    natom_5=`echo ${atom_info} | awk '{print $5}'`

    # And remove one O atom
    natom_5=`echo ${natom_5}-1 | bc`

    # Write new INCAR
    awk -v n1=${natom_1} -v n2=${natom_2} -v n3=${natom_3} -v n4=${natom_4} -v n5=${natom_5} '
        NR == 1 {
            is_changed = 0;
        }
        /NELM/ {
            is_changed = 1;
            printf "   NELM =   200\n";
        }
        /NSW/ {
            is_changed = 1;
            printf "   NSW   =   300\n";
        }
        /IBRION/ {
            is_changed = 1;
            printf "   IBRION =   2\n";
        }
        /ISIF/ {
            is_changed = 1;
            printf "   ISIF   =   2\n";
        }
        /ISPIN/ {
            is_changed = 1;
            printf "   ISPIN = 2\n";
        }
        /MAGMOM/ {
            is_changed = 1;
            is_magmom = 1;
            printf "   MAGMOM = %d*0 %d*0 %d*3 %d*3 %d*0\n", n1, n2, n3, n4, n5;
        }
        /NPAR/ {
            is_changed = 1;
            printf "   NPAR = 4\n";
        }
        /KPAR/ {
            is_changed = 1;
            printf "   KPAR = 4\n";
        }
        /POTIM/ {
            is_changed = 1;
        }
        /NFREE/ {
            is_changed = 1;
        }
        /MAXMIX/ {
            is_changed = 1;
        }
        {if (is_changed == 1){
            is_changed = 0
        } else {
            print $0
        }}
        END {
            if (is_magmom == 0){
                printf "   MAGMOM = %d*0 %d*0 %d*3 %d*3 %d*0\n", n1, n2, n3, n4, n5;
            }
        }
        ' ${i}/INCAR > ${i}/INCAR_vac

    echo ${i} done
done
