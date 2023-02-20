import os
import sys
"""
Usage : python -.py (folder_name)
"""


def main(file_path):
    with open(file_path+'/POSCAR', 'r') as f:
        poscar_lines = f.readlines()
        O_idx = poscar_lines[5].strip().split().index('O')

    with open(file_path+'/INCAR', 'r') as f:
        incar_lines = f.readlines()

    with open(file_path+'/INCAR_vac', 'w') as g:
        for idx, line in enumerate(incar_lines):
            if 'NELM' in line:
                g.write('   NELM = 200\n')
                continue
            elif 'NSW' in line:
                g.write('   NSW = 300\n')
                continue
            elif 'IBRION' in line:
                g.write('   IBRION = 2\n')
                continue
            elif 'ISIF' in line:
                g.write('   ISIF = 2\n')
                continue
            elif 'NPAR' in line:
                g.write('   NPAR = 8\n')
                continue
            elif 'KPAR' in line:
                with open(file_path+'/KPOINTS', 'r') as kpoints:
                    kpoints_lines = kpoints.readlines()
                if kpoints_lines[3].split()[0] == '2':
                    g.write('   KPAR = 2\n')
                continue
            elif 'POTIM' in line:
                continue
            elif 'NFREE' in line:
                continue
            elif 'MAXMIX' in line:
                continue
            elif 'ISPIN' in line:
                g.write('   ISPIN = 2\n')
                continue
            elif 'MAGMOM' in line:
                magmom_line = line.strip().split()
                head_part = magmom_line[0:2]
                tail_part = magmom_line[2:]
                num_O = int(tail_part[O_idx].split('*')[0])
                num_O = str(num_O-1)+'*0'
                tail_part[-1] = num_O
                new_line = ' '.join(head_part + tail_part)
                g.write('   %s\n' % new_line)
                continue
            else:
                g.write(line)


for i in os.listdir(sys.argv[1]):
    path = '%s/%s' % (sys.argv[1], i)
    if not os.path.isdir(path):
        continue
    main(path)
