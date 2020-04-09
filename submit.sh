#!
#!/bin/bash

CONFS='GULF_03'
PATHMT=$SCRATCHDIR/CAL1/msmq_tools

for CONF in $CONFS
do
  sbatch -J $CONF $PATHMT/run.sh $PATHMT/break_saltem.py $PATHMT/${CONF}_param.py
done

