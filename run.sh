#!/bin/bash

#SBATCH -e log_%j-%x.err
#SBATCH -o log_%j-%x.out
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --time=0:30:00
#SBATCH --constraint=VISU
#SBATCH --exclusive

set -e
ulimit -s unlimited

module load intel/17.2
module load python/3.6.3

(date '+%Y/%m/%d %H:%M:%S')
echo python3 -u $@
python3 -u $@
(date '+%Y/%m/%d %H:%M:%S')

