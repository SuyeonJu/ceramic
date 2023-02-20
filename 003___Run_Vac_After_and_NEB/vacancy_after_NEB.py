import os
import sys
import random
import shutil
import numpy as np
from ase import neighborlist
from ase.io import read, write
# import pdb
"""
Make POSCAR_after for O vacancy migration

Precondition : in folder,
    - POSCAR_perfect_cell
    - POSCAR_defect_cell
    - POTCAR, KPOINTS, INCAR, INCAR_NEB
    - batch.j, batch_NEB.j

Usage : python -.py (POSCAR_perfect_cell) (POSCAR_defect)

    Generate POSCARs for O vacancy migration
    by using two POSCARS
    1) perfect POSCAR without any O vacancies
    2) relaxed POSCAR with a single O vacancy

Last modified : 2022. 2. 23
"""


def mk_O_only_POSCAR():
    '''
    Make a POSCAR with O atom only
    '''
    poscar_ref = read(sys.argv[1])

    poscar_O_only = poscar_ref.copy()
    while poscar_O_only:
        poscar_O_only.pop()

    O_positions = {}

    num_atoms_bef_O = 0
    for idx, atom in enumerate(poscar_ref):
        if atom.symbol != 'O':
            num_atoms_bef_O += 1
        else:
            break

    for idx, atom in enumerate(poscar_ref):
        if atom.symbol == 'O':
            O_positions['O_%d' % idx] = atom.position
            poscar_O_only.append(atom)

    return num_atoms_bef_O, poscar_ref, poscar_O_only, O_positions


def get_O_vacancy_idx():
    '''
    Get the index of vacant O atom ("vacancy_idx")
    or can use another method
    '''
    poscar_perfect = read(sys.argv[1])
    poscar_defect = read(sys.argv[2])
    write('POSCAR_i', poscar_defect, format='vasp')

    for idx, atom in enumerate(poscar_defect):
        if atom.symbol != 'O':
            continue

        pos_initial = poscar_perfect[idx].position
        pos_final = atom.position
        displacement = np.linalg.norm(pos_initial-pos_final)

        if displacement > 1.0:
            poscar_perfect_later = poscar_perfect[idx:]
            poscar_defect_later = poscar_defect[idx:]

            is_found = True
            for idx_new, later_atom in enumerate(poscar_defect_later):
                pos_initial_later_atom = later_atom.position
                pos_final_later_atom = poscar_perfect_later[idx_new].position
                displacement_later_atom = np.linalg.norm(
                    pos_initial_later_atom - pos_final_later_atom
                        )

                if displacement_later_atom < 1.0:
                    is_found = False
                    break

            if is_found:
                return idx
            else:
                continue

    return


def mk_POSCAR_after(
        poscar_ref, poscar_O_only, num_atoms_bef_O, vacancy_idx
        ):
    '''
    Make the POSCAR with a O vacancy
    after diffusion
    '''
    # Set cutoff radius
    cutoff = neighborlist.natural_cutoffs(poscar_O_only)

    # Arbitrarily increase cutoff for cations : to make CN of all oxygens be 6
    for idx, _ in enumerate(poscar_O_only):
        cutoff[idx] += 0.79

    # Get neighbor_list for poscar
    nl = neighborlist.NeighborList(
            cutoff, skin=0.01, self_interaction=False, bothways=True
        )
    nl.update(poscar_O_only)

    # From the index of nearest neighbor O atoms,
    # Make defect POSCARs
    indices, offsets = nl.get_neighbors(vacancy_idx - num_atoms_bef_O)

    file_list = []
    for idx in indices:
        idx_before_move = idx + num_atoms_bef_O
        poscar_copy = poscar_ref.copy()
        poscar_copy[idx_before_move].position = \
            poscar_ref[vacancy_idx].position
        poscar_copy.pop(i=vacancy_idx)

        file_name = 'POSCAR_after_O%d_to_O%d' % (
                  vacancy_idx + 1, idx_before_move + 1)
        write(file_name, poscar_copy, format='vasp')
        file_list.append(file_name)

    return file_list


def main():
    '''
    Main function
    '''
    num_atoms_bef_O, poscar_ref, poscar_O_only, O_positions = \
        mk_O_only_POSCAR()
    vacancy_idx = get_O_vacancy_idx()
    file_list = mk_POSCAR_after(
        poscar_ref, poscar_O_only, num_atoms_bef_O, vacancy_idx)

    now_path = os.getcwd()
    selected_case = random.choice(file_list)
    folder_name = '_'.join(selected_case.split('_')[2:])
    new_folder_path = now_path+'/'+folder_name
    os.mkdir(new_folder_path)
    os.mkdir(new_folder_path+'/relax_after')

    # Copy input files for NEB
    shutil.copy(now_path+'/POSCAR_i',
                new_folder_path+'/POSCAR_i')
    shutil.copy(now_path+'/KPOINTS',
                new_folder_path+'/KPOINTS')
    shutil.copy(now_path+'/POTCAR',
                new_folder_path+'/POTCAR')
    shutil.copy(now_path+'/INCAR_NEB',
                new_folder_path+'/INCAR')
    shutil.copy(now_path+'/batch_NEB.j',
                new_folder_path+'/batch_NEB.j')

    # Copy input files for relax_after
    shutil.copy(now_path+'/'+selected_case,
                new_folder_path+'/relax_after/POSCAR')
    shutil.copy(now_path+'/INCAR',
                new_folder_path+'/relax_after/INCAR')
    shutil.copy(now_path+'/POTCAR',
                new_folder_path+'/relax_after/POTCAR')
    shutil.copy(now_path+'/KPOINTS',
                new_folder_path+'/relax_after/KPOINTS')
    shutil.copy(now_path+'/batch.j',
                new_folder_path+'/relax_after/batch.j')

    return


main()
