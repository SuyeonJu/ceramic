import os
import sys
import shutil
"""
Usage : python -.py [folder_path]
"""

def main(main_path):
    current_wd = os.getcwd()

    to_dir = [i for i in os.listdir(main_path)
              if os.path.isdir('%s/%s' % (main_path, i)) and i[0] == 'O'][0]

    os.chdir('%s/%s' %(main_path, to_dir))
    shutil.copy('relax_after/CONTCAR', 'POSCAR_f')
    os.system('nebmake.pl POSCAR_i POSCAR_f 3')
    for i in ['01', '02', '03']:
        shutil.copy('KPOINTS', '%s/KPOINTS' % i)
        shutil.copy('POTCAR', '%s/POTCAR' % i)
        shutil.copy('INCAR', '%s/INCAR' % i)

    os.chdir(current_wd)


for i in os.listdir(sys.argv[1]):
    if not os.path.isdir('%s/%s' %(sys.argv[1], i)):
        continue

    main('%s/%s' %(sys.argv[1], i))
