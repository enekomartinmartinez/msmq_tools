import sys
import numpy as np
from msqg_tools.densities import den_main
from msqg_tools.mask import mask_main
from msqg_tools.average import average_main

params_file = str(sys.argv[1])
exec(open(params_file).read())

ind = [np.arange(nb) for nb in Nb]
gridval = [mlon-3, mlon+3, mlat-3, mlat+3]

#print("GETTING DENSITIES")
#den_main(filename_tem, filename_sal, filename_den,
#         temname, salname, depname, denname, latname, lonname,
#         timname=timname, Nproc=Nproc, ind=ind)
#
#print("COMPUTING MASK")
#mask_main(filename_ssh, filename_mas, latname, lonname,
#          Nproc=1, ind=None, Nb=None)
#
#
#print("COMPUTING AVERAGE DENSITY PROFILE")
#average_main(filename_den, filename_mas, denname, latname, lonname,
#             depname=depname, timname=timname, gridval=gridval, Nproc=Nproc, ind=ind)

print("FINISHED")
