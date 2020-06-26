#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 15:41:38 2020

@author: eneko
"""

##########################################################################
#                            GENERAL PARAMETERS                          #
##########################################################################
# - region: (str)                                                        #
#     Name of the region                                                 #
# - date: (str)                                                          #
#     Initial date of the dataset                                        #
# - Nproc: (int)                                                         #
#     Number of cores to be used                                         #
# - Nb: (tuple of 3 int)                                                 #
#     Number of divisions in z, y, x dimensions                          #
##########################################################################

region = 'OSMOSISc'
date_ini = datetime(2013, 3, 1, 0)
date_fin = datetime(2013, 3, 15, 0)
dates_finuv = datetime(2013, 3, 7, 0)
dates = pd.date_range(start=date_ini, end=date_fin)
dates = dates.strftime('y%Ym%md%d')
datesuv = pd.date_range(start=date_ini, end=date_finuv)
datesuv = dates.strftime('y%Ym%md%d')

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
# - depname: (str)                                                       #
#     Name of the depth variable to be loaded                            #
##########################################################################

path2data = '/mnt/meom/workdir/martiene/DATA/E'+region+'/'
path2uv = '/mnt/meom/workdir/martiene/DATA/EOSMO/speeds/'

filename_tem = path2data + 'NATL60E' + region + '-CJM165_'\
               + date0 + '.1d_votemper'
filename_sal = path2data + 'NATL60E' + region + '-CJM165_'\
               + date0 + '.1d_vosaline'
filename_den = path2data + 'NATL60E' + region + '-CJM165_'\
               + date0 + '.1d_pdens'
filename_str = path2data + 'NATL60E' + region + '-CJM165_'\
               + date0 + '.1d_strheig'
filename_mas = path2data + 'NATL60E' + region + '-CJM165_'\
               + 'mask'

filenames_ssh = [path2data + 'NATL60-CJM165_' + region + '_'
                 + datei + '.1h_SSH' for datei in dates]

filenames_u = [path2uv + 'NATL60EOSMO-CJM165_'
               + datei + '.1d_vozocrtx' for datei in datesuv]

filenames_v = [path2uv + 'NATL60EOSMO-CJM165_'
               + datei + '.1d_vomecrty' for datei in datesuv]

savename_u = [path2data + 'NATL60-CJM165_' + region + '_'
              + datei + '.1d_vozocrtx' for datei in datesuv]
savename_v = [path2data + 'NATL60-CJM165_' + region + '_'
              + datei + '.1d_vomecrty' for datei in datesuv]

filetopo = path2data + 'NATL60-CJM165_'+region+'_mbathy'
filebati = path2data + 'NATL60-CJM165_'+region+'_topo'


sshname = 'sossheig'
uname = 'vozocrtx'
vname = 'vomecrty'
latname = 'nav_lat'
lonname = 'nav_lon'
depname = 'deptht'
batname = 'mbathy'
topname = 'topo'
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

N0 = 256
Nlim = 15
mlat = 48.5
mlon = -20.5
L0 = 750000

##########################################################################
#                      DISCRETIZATION PARAMETERS                         #
##########################################################################
# - method: (str)                                                        #
#     Method to be used to compute discretization                        #
# - plotname: (str)                                                      #
#     Name of discretization plot                                        #
# - paramsname: (str)                                                    #
#     Name of the params output file                                     #
# - p: (positive int)                                                    #
#     p-norm to compute the maximum method                               #
# - depl: ((float, float))                                               #
#     Minimum depth of first layer, maximum depth of last layer          #
# - nlsep: (int)                                                         #
#     Minimum input layers separation between output two layers          #
# - nl: (int)                                                            #
#     Number of layers to be computed                                    #
##########################################################################

method = 'max'
plotname = region + '_' + dates[0] + '.png'
paramsname = region + '_' + dates[0] + '_params.in'
p = 2
depl = (100, 200)
nlsep = 1
nl = 2


##########################################################################
#                           PHYSICAL PARAMETERS                          #
##########################################################################
# - H: (float)                                                           #
#     Total vertical height                                              #
# - L: (float)                                                           #
#     Horizontal lenght scale                                            #
# - U: (float)                                                           #
#     Horizontal velocity scale                                          #
# - g: (float)                                                           #
#     Gravity                                                            #
# - den0: (float)                                                        #
#     Reference density                                                  #
# - Ekb: (float)                                                         #
#     Ekman bottom friction                                              #
# - Re: (float)                                                          #
#     Reynolds number                                                    #
# - Re4: (float)                                                         #
#     Biharmonic Reynolds number                                         #
# - tau0: (float)                                                        #
#     Non dimensional wind stress                                        #
# - DT: (float)                                                          #
#     Non dimensional time step                                          #
# - tend: (float)                                                        #
#     Non dimensional final time                                         #
# - dtout: (float)                                                       #
#     Non dimensional output time                                        #
# - CFL: (float)                                                         #
#     CFL constant                                                       #
##########################################################################

H = 4500.
L = 50000.
U = .1
g = 9.81
den0 = 1027.

Ekb = 0.001
Re = 1000.
Re4 = 0
tau0 = 0.

DT = 0.0003
tend = 2000.
dtout = 1.
CLF = .5