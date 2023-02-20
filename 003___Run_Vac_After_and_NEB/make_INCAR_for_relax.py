from collections import OrderedDict
import sys
import os
import shutil
"""
Usage : python -.py {folder_path}
"""

def main(INCAR_path, INCAR_out):
    with open(INCAR_path, 'r') as f:
        lines = f.readlines()

    # Set Default settings
    INCAR_dict = OrderedDict()
    INCAR_dict["Starting parameters"] = OrderedDict()
    INCAR_dict["Starting parameters"]["NWRITE"] = '2'
    INCAR_dict["Starting parameters"]["ISTART"] = '0'
    INCAR_dict["Starting parameters"]["ICHARG"] = '2'
    INCAR_dict["Starting parameters"]["INIWAV"] = '1'

    INCAR_dict["Electronic relaxation"] = OrderedDict()
    INCAR_dict["Electronic relaxation"]["ENCUT"] = '520'
    INCAR_dict["Electronic relaxation"]["PREC"] = 'Accurate'
    INCAR_dict["Electronic relaxation"]["ADDGRID"] = '.F.'
    INCAR_dict["Electronic relaxation"]["NELM"] = '200'
    INCAR_dict["Electronic relaxation"]["EDIFF"] = '1E-06'
    INCAR_dict["Electronic relaxation"]["LREAL"] = 'Auto'
    INCAR_dict["Electronic relaxation"]["ALGO"] = 'Normal'
    INCAR_dict["Electronic relaxation"]["LWAVE"] = '.F.'
    INCAR_dict["Electronic relaxation"]["LCHARG"] = '.F.'

    INCAR_dict["Ionic relaxation"] = OrderedDict()
    INCAR_dict["Ionic relaxation"]["NSW"] = '300'
    INCAR_dict["Ionic relaxation"]["IBRION"] = '2'
    INCAR_dict["Ionic relaxation"]["EDIFFG"] = '-0.05'
    INCAR_dict["Ionic relaxation"]["ISIF"] = '2'
    INCAR_dict["Ionic relaxation"]["ISYM"] = '1'
    # INCAR_dict["Ionic relaxation"]["POTIM"] = '0'

    INCAR_dict["LDA+U settings"] = OrderedDict()

    INCAR_dict["DOS related values"] = OrderedDict()
    INCAR_dict["DOS related values"]["ISMEAR"] = '0'
    INCAR_dict["DOS related values"]["SIGMA"] = '0.05'
    INCAR_dict["DOS related values"]["LORBIT"] = '11'

    INCAR_dict["Calculation settings"] = OrderedDict()
    INCAR_dict["Calculation settings"]["NPAR"] = '8'
#    INCAR_dict["Calculation settings"]["KPAR"] = '2'

    INCAR_dict["Spin-polarized calculation"] = OrderedDict()

    # Read INCAR settings
    for line in lines:
#        if 'EDIFF ' in line:
#            EDIFF_idx = line.split().index('=') + 1
#            EDIFF = line.split()[EDIFF_idx]
#            INCAR_dict["Electronic relaxation"]["EDIFF"] = EDIFF
        if 'EDIFFG ' in line:
            EDIFFG_idx = line.split().index('=') + 1
            EDIFFG = line.split()[EDIFFG_idx]
            INCAR_dict["Ionic relaxation"]["EDIFFG"] = EDIFFG
#        if 'ALGO ' in line:
#            ALGO_idx = line.split().index('=') + 1
#            ALGO = line.split()[ALGO_idx]
#            INCAR_dict["Electronic relaxation"]["ALGO"] = ALGO
        if 'LDAU' in line or 'LMAX' in line:
            param = line.split()[0]
            param_value = line.strip('\n').split()[2:]
            INCAR_dict["LDA+U settings"][param] = ' '.join(param_value)
        if 'ISPIN' in line or 'MAGMOM' in line:
            param = line.split()[0]
            param_value = line.strip('\n').split()[2:]
            INCAR_dict["Spin-polarized calculation"][param] = ' '.join(param_value)

    with open(INCAR_out, 'w') as g:
        g.write('\n Starting parameters for this run:\n')
        for key, value in INCAR_dict["Starting parameters"].items():
            g.write('   %s = %s\n' % (key, value))

        g.write('\n Electronic Relaxation:\n')
        for key, value in INCAR_dict["Electronic relaxation"].items():
            g.write('   %s = %s\n' % (key, value))

        g.write('\n Ionic Relaxation:\n')
        for key, value in INCAR_dict["Ionic relaxation"].items():
            g.write('   %s = %s\n' % (key, value))

        g.write('\n LDA+U settings:\n')
        for key, value in INCAR_dict["LDA+U settings"].items():
            g.write('   %s = %s\n' % (key, value))

        g.write('\n DOS related values:\n')
        for key, value in INCAR_dict["DOS related values"].items():
            g.write('   %s = %s\n' % (key, value))

        g.write('\n Calculation settings:\n')
        for key, value in INCAR_dict["Calculation settings"].items():
            g.write('   %s = %s\n' % (key, value))

        g.write('\n Spin-polarized calculations:\n')
        for key, value in INCAR_dict["Spin-polarized calculation"].items():
            g.write('   %s = %s\n' % (key, value))


for f in os.listdir(sys.argv[1]):
    path = '%s/%s' % (sys.argv[1], f)
    if not os.path.isdir(path):
        continue

    main(path+'/INCAR', path+'/INCAR_new')
    shutil.move(path+'/INCAR', path+'/INCAR_original')
    shutil.move(path+'/INCAR_new', path+'/INCAR')
    print('%s Done' % path)
