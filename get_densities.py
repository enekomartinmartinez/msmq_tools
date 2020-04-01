import sys
import numpy as np
from msmq_tools.densities import den_main

params_file = str(sys.argv[1])
exec(open(params_file).read())

ind = [np.arange(nb) for nb in Nb]

den_main(filename_tem, filename_sal, filename_den,
         temname, salname, depname, denname, latname, lonname,
         timname=timname, Nproc=Nproc, ind=ind)
