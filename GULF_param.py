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
date_ini = datetime(2013, 3, 13, 0)
date_fin = datetime(2013, 3, 31, 0)
dates = pd.date_range(start=date_ini, end=date_fin)
dates = dates.strftime('y%Ym%md%d')

Nproc = 1


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

filenames_ssh = [path2data + 'NATL60-CJM165_' + region + '_'
                 + datei + '.1h_SSH' for datei in dates]

sshname = 'sossheig'
latname = 'lat'
lonname = 'lon'
timname = 'time'


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

