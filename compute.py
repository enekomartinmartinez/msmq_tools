import sys
import numpy as np
from datetime import datetime
import matplotlib as mpl
mpl.use('Agg')
import msqg_tools as mt

params_file = str(sys.argv[1])
exec(open(params_file).read())

ind = [np.arange(nb) for nb in Nb]
gridval = [mlon-3, mlon+3, mlat-3, mlat+3]

print("\n\n")
print(datetime.now())
print("\n")
print("INTERPOLATING SSH DATA")
mt.int_main(filenames_ssh, [sshname],
            latname, lonname, mlat, mlon,
            L0, N0, Nlim,
            None, timname,
            'cubic', Nproc, parallel='time')

# SPLITTING S AND T DATA
# Computed in other machine

#print("\n\n")
#print(datetime.now())
#print("\n")
#print("GETTING DENSITIES")
#mt.den_main(filename_tem, filename_sal, filename_den,
#            temname, salname, depname, denname, latname, lonname,
#            timname=timname, Nproc=Nproc, ind=ind)
#
#
#print("\n\n")
#print(datetime.now())
#print("\n")
#print("COMPUTING MASK")
#mt.mask_main(filenames_ssh[0], filename_mas, latname, lonname,
#             Nproc=1, ind=None, Nb=Nb)
#
#
#print("\n\n")
#print(datetime.now())
#print("\n")
#print("COMPUTING AVERAGE DENSITY PROFILE")
#mt.average_main(filename_den, filename_mas, denname, latname, lonname,
#                depname=depname, timname=timname, gridval=gridval, 
#                Nproc=Nproc, ind=ind)
#
#
#print("\n\n")
#print(datetime.now())
#print("\n")
#print("COMPUTING DISCRETIZATION")
#mt.partition_main(filename_den+'_mean', denname, 
#                  depname, latname, lonname,
#                  paramsname, ind, nl, N0, L0, timname,
#                  method, plotname, nlsep, p,
#                  depl, False,
#                  H, L, U, g, den0,
#                  Ekb, Re, Re4, tau0,
#                  DT, tend, dtout, CLF)
#
#
#print("\n\n")
#print(datetime.now())
#print("\n")
#print("COMPUTING STRATIFICATION")
## TO DO
#

print("\n\n")
print(datetime.now())
print("\n")
print("COMPUTING INI FILE")
mt.genini_main(filenames_ssh[0], [sshname], latname, lonname, mlat, mlon,
               L0, N0, Nlim)


print("\n\n")
print(datetime.now())
print("\n")
print("FINISHED")
