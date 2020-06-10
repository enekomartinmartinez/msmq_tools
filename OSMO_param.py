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

region = 'OSMOSISb'
date_ini = datetime(2013, 3, 1, 0)
date_fin = datetime(2013, 3, 7, 0)
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
path2uv = '/mnt/meom/workdir/martiene/DATA/EOSMO/speeds/'

filenames_ssh = [path2data + 'NATL60-CJM165_' + region + '_'
                 + datei + '.1h_SSH' for datei in dates]

filenames_u = [path2uv + 'NATL60EOSMO-CJM165_'
               + datei + '.1d_vozocrtx' for datei in dates]

filenames_v = [path2uv + 'NATL60EOSMO-CJM165_'
               + datei + '.1d_vomecrty' for datei in dates]

savename_u = [path2data + 'NATL60-CJM165_' + region + '_'
              + datei + '.1d_vozocrtx' for datei in dates]
savename_v = [path2data + 'NATL60-CJM165_' + region + '_'
              + datei + '.1d_vomecrty' for datei in dates]

sshname = 'sossheig'
uname = 'vozocrtx'
vname = 'vomecrty'
latname = 'nav_lat'
lonname = 'nav_lon'
depname = 'deptht'
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
mlat = 50.5
mlon = -20.
L0 = 1300000


N0 = 256
Nlim = 15
mlat = 50.5
mlon = -20.
L0 = 1300000
