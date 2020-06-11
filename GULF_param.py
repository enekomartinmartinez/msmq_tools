from datetime import datetime
import pandas as pd

##########################################################################
#                            GENERAL PARAMETERS                          #
##########################################################################
# - region: (str)                                                        #
#     Name of the region                                                 #
# - date: (str)                                                          #
#     Initial date of the dataset                                        #
# - Nproc: (int)                                                         #
#     Number of cores to be used                                         #
##########################################################################

region = 'GULFSTREAMb'
date_ini = datetime(2012, 10, 1, 0)
date_fin = datetime(2013, 9, 30, 0)
dates = pd.date_range(start=date_ini, end=date_fin)
dates = dates.strftime('y%Ym%md%d')

Nproc = 1
Nb = (1, 10, 10)

##########################################################################
#                            LOADING PARAMETERS                          #
##########################################################################
# - path2data: (str)                                                     #
#     Path to the original data                                          #
# - filename: (str)                                                      #
#     Name of the file to be loaded                                      #
# - varname: (list(str))                                                 #
#     Name of the variables to be loaded                                 #
# - latname: (str)                                                       #
#     Name of the latitude to be loaded                                  #
# - lonname: (str)                                                       #
#     Name of the longitude to be loaded                                 #
# - timname: (str)                                                       #
#     Name of the time variable to be loaded                             #
##########################################################################


path2data = '/mnt/meom/workdir/martiene/DATA/'+region+'/'
path2uv = '/mnt/meom/workdir/martiene/DATA/EGULF/speeds/'

filenames_ssh = [path2data + 'NATL60-CJM165_' + region + '_'
                 + datei + '.1h_SSH' for datei in dates]

filenames_u = [path2uv + 'NATL60EGULF-CJM165_'
               + datei + '.1d_vozocrtx' for datei in dates]

filenames_v = [path2uv + 'NATL60EGULF-CJM165_'
               + datei + '.1d_vomecrty' for datei in dates]

savename_u = [path2data + 'NATL60-CJM165_' + region + '_'
              + datei + '.1d_vozocrtx' for datei in dates]
savename_v = [path2data + 'NATL60-CJM165_' + region + '_'
              + datei + '.1d_vomecrty' for datei in dates]

filetopo = path2data + 'NATL60-CJM165_'+region+'_mbathy'
filebati = path2data + 'NATL60-CJM165_'+region+'_topo'


sshname = 'sossheig'
uname = 'vozocrtx'
vname = 'vomecrty'
latname = 'nav_lat'
lonname = 'nav_lon'
depname = 'deptht'
batname = 'mbathy'
timname = 'time_counter'


##########################################################################
#                      INTERPOLATION PARAMETERS                          #
##########################################################################
# - N0: (power of 2)                                                     #
#     Number of gridpoints of the model                                  #
# - Nlim: (int <<N0)                                                     #
#     Number of gridpoints that will be left in the boundary             #
# - mlat: (float)                                                        #
#     Mean latitude for the output grid                                  #
# - mlon: (float)                                                        #
#     Mean longitude for the output grid                                 #
# - L0: (float)                                                          #
#     Total longitude for the output                                     #
##########################################################################

N0 = 512
Nlim = 30
mlat = 36.5
mlon = -56.
L0 = 1700000

N0 = 256
Nlim = 15
mlat = 38.
mlon = -57.5
L0 = 1300000
