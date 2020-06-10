import sys
import numpy as np
from datetime import datetime
import matplotlib as mpl
import msqg_tools as mt

mpl.use('Agg')


params_file = str(sys.argv[1])
exec(open(params_file).read())

ind = [np.arange(nb) for nb in Nb]
gridval = [mlon-3, mlon+3, mlat-3, mlat+3]

#print("\n\n")
#print(datetime.now())
#print("\n")
#print("INTERPOLATING SSH DATA")
#mt.int_main(filenames_ssh, [sshname],
#            latname, lonname, mlat, mlon,
#            L0, N0, Nlim,
#            None, timname,
#            'cubic', Nproc, parallel='time')

#print("\n\n")
#print(datetime.now())
#print("\n")
#print("INTERPOLATING U, V DATA")

filetopo = '/mnt/meom/workdir/martiene/DATA/OSMOSISb/NATL60-CJM165_OSMOSISb_mbathy'
mt.topo_main(filetopo, 'save', 'mbathy', latname, lonname,
             'nav_lev', timname)

#print("\n\n")
#print(datetime.now())
#print("\n")
#print("INTERPOLATING U, V DATA")
#for filei, sname in zip(filenames_u, savename_u):
#    mt.vaverage_main(filei, sname, uname, latname, lonname,
#                     depname, timname, (186, 6000),
#                     Nproc, ind)
#
#mt.int_main(savename_u, [uname],
#            latname, lonname, mlat, mlon,
#            L0, N0, Nlim,
#            None, timname,
#            'cubic', Nproc,
#            parallel='time', ind=ind)
#
#for filei, sname in zip(filenames_v, savename_v):
#    mt.vaverage_main(filei, sname, vname, latname, lonname,
#                     depname, timname, (186, 6000),
#                     Nproc, ind)
#
#mt.int_main(savename_v, [vname],
#            latname, lonname, mlat, mlon,
#            L0, N0, Nlim,
#            None, timname,
#            'cubic', Nproc,
#            parallel='time', ind=ind)

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
#method = 'dep'
#depl = (200, 1000)
#depl = [2000]
#print("\n\n")
#print(datetime.now())
#print("\n")
#print("COMPUTING DISCRETIZATION")
#bden = mt.partition_main(filename_den+'_mean', denname,
#                         depname, latname, lonname,
#                         paramsname, nl, N0, L0, timname,
#                         method, plotname, nlsep, p,
#                         depl, False,
#                         H, L, U, g, den0,
#                         Ekb, Re, Re4, tau0,
#                         DT, tend, dtout, CLF)
#

#print("\n\n")
#print(datetime.now())
#print("\n")
#print("COMPUTING STRATIFICATION")
#mt.stra_main(filename_den, filename_str, bden,
#             denname, latname, lonname, depname,
#             strname, timname, Nproc, ind, H)
#
#print("\n\n")
#print(datetime.now())
#print("\n")
#print("COMPUTING INI FILE")
#mt.genini_main(filenames_ssh[0], [sshname], latname, lonname, mlat, mlon,
#               L0, N0, Nlim)


print("\n\n")
print(datetime.now())
print("\n")
print("FINISHED")
