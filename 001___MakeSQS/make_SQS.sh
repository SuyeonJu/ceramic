#!/bin/sh
#PBS -l nodes=1:g2:ppn=1
#PBS -N SQS
##PBS -l walltime=00:00:30

cd $PBS_O_WORKDIR
cat $PBS_NODEFILE > nodefile
NPROC=`wc -l < $PBS_NODEFILE`

corrdump -l=rndstr.in -ro -noe -nop -clus -2=0.9 -3=0.9
cp ../sqscell.out .
mcsqs -rc
