import sys
import dask
import numpy as np
from datetime import datetime
import matplotlib as mpl
mpl.use('Agg')
import msqg_tools as mt

params_file = str(sys.argv[1])
exec(open(params_file).read())

filenames = [filename_sal_occi, filename_tem_occi]
varnames = [salname, temname]

print("\n\n")
print(datetime.now())
print("\n")

print("SPLITTING S AND T DATA")
def split(iii):
    mt.breakds(filenames[iii], [varnames[iii]],
               latname, lonname,
               Nb, None,
               depname, timname)
    return 1

output = []
for i in range(2):
    run_paral = dask.delayed(split)(i)
    output.append(run_paral)
total = dask.delayed(sum)(output)
total.compute()

print("\n\n")
print(datetime.now())
print("\n")
print("FINISHED")
