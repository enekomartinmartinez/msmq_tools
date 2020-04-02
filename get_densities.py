import sys
import numpy as np
from msqg_tools.densities import den_main
from msqg_tools.mask import mask_main

params_file = str(sys.argv[1])
exec(open(params_file).read())

#ind = [np.arange(nb) for nb in Nb]
#
#den_main(filename_tem, filename_sal, filename_den,
#         temname, salname, depname, denname, latname, lonname,
#         timname=timname, Nproc=Nproc, ind=ind)

mask_main(filename_ssh, filename_mas, latname, lonname,
          Nproc=1, ind=None, Nb=Nb)

print("FINISH")
