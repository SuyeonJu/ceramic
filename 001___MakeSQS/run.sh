#!/bin/sh
for i in {1..24};do
    cd composition_$i
    sed '/nodes/s/g2/g1/g' ../make_SQS.sh > ./make_SQS.sh
    qsub make_SQS.sh
    cd ..
done
for i in {25..48};do
    cd composition_$i
    sed '/nodes/s/g2/g2/g' ../make_SQS.sh > ./make_SQS.sh
    qsub make_SQS.sh
    cd ..
done
for i in {49..76};do
    cd composition_$i
    sed '/nodes/s/g2/g3/g' ../make_SQS.sh > ./make_SQS.sh
    qsub make_SQS.sh
    cd ..
done
for i in {77..88};do
    cd composition_$i
    sed '/nodes/s/g2/g4/g' ../make_SQS.sh > ./make_SQS.sh
    qsub make_SQS.sh
    cd ..
done
for i in {89..96};do
    cd composition_$i
    sed '/nodes/s/g2/g2/g' ../make_SQS.sh > ./make_SQS.sh
    qsub make_SQS.sh
    cd ..
done
