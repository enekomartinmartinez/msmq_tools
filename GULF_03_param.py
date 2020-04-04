##########################################################################
#                            GENERAL PARAMETERS                          #
##########################################################################
# - region: (str)                                                        #
#     Name of the region where the interpolation is done                 #
# - parallel: (bool)                                                     #
#     True for parallelize interpolation in time dimension               #
# - Nproc: (int)                                                         #
#     Number of cores to be used                                         #
##########################################################################

region = 'GULF'
date = 'y2010m03d01'
dateL = 'X_1h_20100220_20100316'
dateR = '20100301-20100301'
parallel = True
Nproc = 3


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

path2data = '/mnt/meom/workdir/martiene/DATA/E'+region+'/'

filename_tem = path2data + 'eNATL60E' + region + '-BLBT02'\
               + dateL + '_gridT_' + dateR
filename_sal = path2data + 'eNATL60E' + region + '-BLBT02'\
               + dateL + '_gridS_' + dateR
filename_den = path2data + 'eNATL60E' + region + '-BLBT02'\
               + dateL + '_gridD_' + dateR
filename_mas = path2data + 'eNATL60E' + region + '-BLBT02_'\
               + 'mask'
filename_ssh = path2data + 'eNATL60E' + region + '-BLBT02_'\
               + date + '.1h_sossheig'

sshname = 'sossheig'
temname = 'votemper'
salname = 'vosaline'
denname = 'pdens'
latname = 'nav_lat'
lonname = 'nav_lon'
timname = 'time_counter'
depname = 'deptht'


##########################################################################
#                      INTERPOLATION PARAMETERS                          #
##########################################################################
# - N0: (power of 2)                                                     #
#     Number of gridpoints of the model                                  #
# - Nlim: (int <<N0)                                                     #
#     Number of gridpoints that will be left in the boundary             #
# - giveboundary: (bool)                                                 #
#     True for complete the boundary with linear values, 0 in the border #
# - mlat: (float)                                                        #
#     Mean latitude for the output grid                                  #
# - mlon: (float)                                                        #
#     Mean longitude for the output grid                                 #
# - L0: (float)                                                          #
#     Total longitude for the output                                     #
##########################################################################

N0 = 512
Nlim = 20
giveboundary = False
mlat = 37.
mlon = -57.
L0 = 1600000
H = 4500.
L = 50000.
U = .1
g = 9.81
den0 = 1029
Ekb = 0.
Re = 0.
Re4 = 0
tau0 = 0.,
DT = 5e-4
tend = 2000.
dtout = 1.
CLF = .5
method = 'max'
plotname = region + '_' + date + '.png'
nlsep = 1
p = 2
depl = (500, 2000)
nl = 2
paramsname = region + '_' + date + '_params.in'

##########################################################################
#                           SAVING PARAMETERS                            #
##########################################################################
# - path2save: (str)                                                     #
#     Path where the data will be saved                                  #
# - savename: (str)                                                      #
#     Saving name                                                        #
##########################################################################

path2save = path2data


##########################################################################
#                            SPLITING PARAMETERS                         #
##########################################################################
# - split: (bool)                                                        #
#     True for split the data in sub-boxes                               #
# - Nb: (tuple of 3 int)                                                 #
#     Number of divisions in z, y, x dimensions                          #
##########################################################################

split = False
Nb = (1, 10, 10)

