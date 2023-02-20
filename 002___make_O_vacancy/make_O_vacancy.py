from ase import Atoms
from ase.io import read, write
from ase import neighborlist
import os
import sys
"""
make all possible defect structures with a single oxygen vacancy
for a given structure (especially for perovskite structures)

Usage : python -.py (dir_path)
Last modified : 2021.12.08
"""

folder_path = os.listdir(sys.argv[1])


def make_defect_structures(poscar_path, skin_depth=0.7):
    '''
    Make defect structures for a given poscar
    '''
    # Read all atom data from perfect structure
    poscar = read(poscar_path+'/POSCAR')

    # Set cutoff radius for each atom
    cutoff = neighborlist.natural_cutoffs(poscar)
    for i in range(len(poscar)):
        if poscar[i].symbol != 'O':
            # Arbitrarily increase cutoff for cations
            # to make CN of all oxygens be 6
            cutoff[i] += skin_depth

    # Get neighbor_list for poscar
    neighbor_list = neighborlist.NeighborList(
        cutoff, self_interaction=False, bothways=True)
    neighbor_list.update(poscar)

    # get connectivity matrix as numpy matrix form (scipy form if sparse=True)
    matrix = neighbor_list.get_connectivity_matrix(sparse=False)

    # Classify each oxygen atom by their neighbor info
    O_vacancy_type = ['' for i in range(len(matrix))]
    for row in range(len(matrix)):
        if poscar[row].symbol != 'O':
            continue

        neighbor_tmp = Atoms('', [], pbc=True, cell=poscar.get_cell())
        for col in range(len(matrix[row])):
            if matrix[row][col] == 1:
                if poscar[col].symbol == 'O':
                    continue
                neighbor_tmp.append(poscar[col])

        O_vacancy_type[row] = neighbor_tmp.get_chemical_formula()

    O_counter = 0
    # For each type of oxygen, make defect structure and write poscar
    for idx, vac_type in enumerate(O_vacancy_type):
        if vac_type == '':
            continue

        poscar_copy = poscar.copy()
        poscar_copy.pop(i=idx)
        file_counter = 0

        if not os.path.isdir(poscar_path+'/%s/' % vac_type):
            os.makedirs(poscar_path+'/%s/' % vac_type)

        title = 'POSCAR_' + vac_type + '_%d' % file_counter

        while os.path.isfile(poscar_path+'/%s/' % vac_type + title):
            file_counter += 1
            title = 'POSCAR_' + vac_type + '_%d' % file_counter

        O_counter += 1
        write(
            poscar_path+'/%s/' % vac_type + title,
            poscar_copy,
            format='vasp',
            direct=True,
            label='O Vacancy idx = %d' % O_counter
        )

    return


for item in folder_path:
    make_defect_structures(sys.argv[1]+'/%s' % item)
    print(sys.argv[1]+'%s Done' % item)
