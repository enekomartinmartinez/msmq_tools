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

region = 'OSMO'
date = (2012, 10, 1)
dates = ['y' + str(date[0])
         + 'm' + str(date[1]).zfill(2)
         + 'd' + str(date[2]+i).zfill(2)
         for i in range(31)]

date0 = dates[0]

Nproc = 2
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
filenames_ssh = [path2data + 'NATL60E' + region + '-CJM165_'
                 + datei + '.1h_sossheig' for datei in dates]

sshname = 'sossheig'
temname = 'votemper'
salname = 'vosaline'
denname = 'pdens'
latname = 'nav_lat'
lonname = 'nav_lon'
timname = 'time_counter'
depname = 'deptht'
strname = 'strheig'


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
depl = (500, 2000)
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

H = 4000.
L = 50000.
U = .1
g = 9.81
den0 = 1029.

Ekb = 0.
Re = 0.
Re4 = 0
tau0 = 0.

DT = 5e-4
tend = 2000.
dtout = 1.
CLF = .5
