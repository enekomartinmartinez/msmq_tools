#!
#!/bin/bash

if [ $1 = all ];
then
  echo 'OMP_NUM_THREADS=4 nohup bash pylaunchall.sh > log_all.out 2>&1 &'
  OMP_NUM_THREADS=4 nohup bash pylaunchall.sh > log_all.out 2>&1 &
else
  echo 'OMP_NUM_THREADS=4 nohup python3 -u compute.py $1_param.py > log_$1.out 2>&1 &'
  OMP_NUM_THREADS=4 nohup python3 -u compute.py $1_param.py > log_$1.out 2>&1 &
fi
