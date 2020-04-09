#!
#!/bin/bash

CONFS='GULF_03 GULF_09 OSMO_03 OSMO_09'

for CONF in $CONFS
do
    sbatch -J $CONF $SCRATCHDIR/run2.sh $SCRATCHDIR/CAL1/msqg_tools/break_saltem.py $CONF
done
