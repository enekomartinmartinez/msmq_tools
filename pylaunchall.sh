
CONFS='GULF_03 GULF_10 OSMO_03 OSMO_10'

for CONF in $CONFS
do
  echo python3 -u compute.py ${CONF}_param.py
  python3 -u compute.py ${CONF}_param.py
done
