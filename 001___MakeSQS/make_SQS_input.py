import os,sys
import shutil

with open(sys.argv[1],'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if not i: # for the 1st line
        dat = line.split()
        A_elem = dat[1:3]
        B_elem = dat[3:5]
        continue

    dat = line.split()
    comp_A = "%s=%.8f,%s=%.8f" %(A_elem[0],float(dat[1]),A_elem[1],float(dat[2]))
    comp_B = "%s=%.8f,%s=%.8f" %(B_elem[0],float(dat[3]),B_elem[1],float(dat[4]))

    os.mkdir('composition_%d' % i)
    with open('composition_%d/rndstr.in' % i,'w') as output:
        output.write('1 1.0186 1.4215 90 90 90\n')
        output.write('1 0 0\n')
        output.write('0 1 0\n')
        output.write('0 0 1\n')
        output.write('0.5093295335885202 0.5435348261436559 0.7500000000000000 %s\n' % comp_A)
        output.write('0.4906704664114798 0.4564651738563441 0.2500000000000000 %s\n' % comp_A)
        output.write('0.9906704664114798 0.0435348261436559 0.7500000000000000 %s\n' % comp_A)
        output.write('0.0093295335885202 0.9564651738563441 0.2500000000000000 %s\n' % comp_A)
        output.write('0.0000000000000000 0.5000000000000000 0.5000000000000000 %s\n' % comp_B)
        output.write('0.0000000000000000 0.5000000000000000 0.0000000000000000 %s\n' % comp_B)
        output.write('0.5000000000000000 0.0000000000000000 0.5000000000000000 %s\n' % comp_B)
        output.write('0.5000000000000000 0.0000000000000000 0.0000000000000000 %s\n' % comp_B)
        output.write('0.0790865065330095 0.4799553198193749 0.7500000000000000 O\n')
        output.write('0.9209134934669905 0.5200446801806251 0.2500000000000000 O\n')
        output.write('0.4209134934669905 0.9799553198193749 0.7500000000000000 O\n')
        output.write('0.5790865065330095 0.0200446801806251 0.2500000000000000 O\n')
        output.write('0.7912792215532036 0.7905481202149716 0.9583129659406922 O\n')
        output.write('0.2087207784467964 0.2094518797850284 0.4583129659406922 O\n')
        output.write('0.2087207784467964 0.2094518797850284 0.0416870340593078 O\n')
        output.write('0.7912792215532036 0.7905481202149716 0.5416870340593078 O\n')
        output.write('0.7087207784467964 0.2905481202149716 0.9583129659406922 O\n')
        output.write('0.2912792215532036 0.7094518797850284 0.4583129659406922 O\n')
        output.write('0.2912792215532036 0.7094518797850284 0.0416870340593078 O\n')
        output.write('0.7087207784467964 0.2905481202149716 0.5416870340593078 O\n')
