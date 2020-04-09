#!
#!/bin/bash

OMP_NUM_THREADS=4 

nohup python3 -u compute.py $1_param.py > log_$1.out 2>&1 &
