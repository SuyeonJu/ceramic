# Move folders whose calculations are finished
done_folder='/scratch/x2294a07/SOFC/101___Vacancy_Done'
for i in Doped_Ce/*;do
#    done_or_not=`tail ${i}/selected_vac/stdout.x | grep fatal | wc -l`
    done_or_not=`grep reached ${i}/selected_vac/stdout.x | wc -l`
    if (( ${done_or_not} ));then
        mv ${i} ${done_folder}
    fi
done
