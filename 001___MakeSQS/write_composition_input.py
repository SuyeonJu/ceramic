with open('test','w')as f:
    f.write('#\tCa\tSr\tTi\tZr\tO\n')
    counter = 0
    for i in range(16):
        for j in range(6):
            counter += 1
            doping_A = (i+1)/32
            doping_B = (j+1)/32
            f.write('%d\t%.8f\t%.8f\t%.8f\t%.8f\t3\n' %(counter,1-doping_A,doping_A,1-doping_B,doping_B))
