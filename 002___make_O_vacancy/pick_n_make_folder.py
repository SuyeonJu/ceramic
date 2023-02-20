import numpy as np
import os
import sys
import shutil
"""
1) pick one POSCAR from all POSCARs with one O vacancy
2) make folder with batchfile
"""

##########
batch_path = '/scratch/x2294a07/SOFC/003___Vacancy_run/batch_nurion.j'
##########


def pick_poscar(poscar_path, criteria):
    '''
    pick a poscar with given criteria
    '''
    vac_folder_list = [
        i for i in os.listdir(poscar_path)
        if os.path.isdir(poscar_path+'/'+i)
    ]
    vac_poscar_list = []
    # list up all poscars with given criteria
    for idx, vac_folder in enumerate(vac_folder_list):
        if criteria in vac_folder:
            vac_poscar_list += [
                '%s/%s' % (vac_folder, vac_poscar)
                for vac_poscar in os.listdir(poscar_path+'/'+vac_folder)
            ]
    # choose random poscar
    selected_poscar = np.random.choice(vac_poscar_list)

    # make directory
    os.mkdir(poscar_path+'/selected_vac')
    shutil.copy(poscar_path+'/INCAR_vac', poscar_path+'/selected_vac/INCAR')
    shutil.copy(poscar_path+'/POTCAR', poscar_path+'/selected_vac/POTCAR')
    shutil.copy(poscar_path+'/KPOINTS', poscar_path+'/selected_vac/KPOINTS')
    shutil.copy(poscar_path+'/'+selected_poscar,
                poscar_path+'/selected_vac/POSCAR')
    shutil.copy(batch_path, poscar_path+'/selected_vac/batch.j')


for item in os.listdir(sys.argv[1]):
    if ('BCTZ' in item) or ('CSTZ' in item):
        pick_poscar(sys.argv[1]+'/'+item, 'Ti2')
    elif ('BSCF' in item) or ('LSCF' in item):
        pick_poscar(sys.argv[1]+'/'+item, 'Co2')
    elif ('Doped_Ce' in item):
        pick_poscar(sys.argv[1]+'/'+item, 'Ce2')
