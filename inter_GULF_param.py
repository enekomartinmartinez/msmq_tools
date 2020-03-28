###############################################################################
#                       PARAMETERS FOR INTERPOLATION                          #
###############################################################################
# - region: (str)                                                             #
#     Name of the region where the interpolation is done                      #
# - parallel: (bool)                                                          #
#     True for parallelize interpolation in time dimension                    #
###############################################################################

region = 'GULF'
parallel = True


###############################################################################
#                            LOADING PARAMETERS                               #
###############################################################################
# - path2data: (str)                                                          #
#     Path to the original data                                               #
# - filename: (str)                                                           #
#     Name of the file to be loaded                                           #
# - varname: (list(str))                                                      #
#     Name of the variables to be loaded                                      #
# - latname: (str)                                                            #
#     Name of the latitude to be loaded                                       #
# - lonname: (str)                                                            #
#     Name of the longitude to be loaded                                      #
# - timname: (str)                                                            #
#     Name of the time variable to be loaded                                  #
###############################################################################

path2data = '/scratch/cnt0024/hmg2840/albert7a/eNATL60/'
            + 'eNATL60-BLBT02-S/1h/E' + region + '/'

filename = None
varnames = [None]
latname = 'nav_lat'
lonname = 'nav_lon'
timname = 'time_counter'


###############################################################################
#                            OUTPUT PARAMETERS                                #
###############################################################################
# - N0: (power of 2)                                                          #
#     Number of gridpoints of the model                                       #
# - Nlim: (int <<N0)                                                          #
#     Number of gridpoints that will be left in the boundary                  #
# - giveboundary: (bool)                                                      #
#     True for complete the boundary with linear values, 0 in the border      #
# - mlat: (float)                                                             #
#     Mean latitude for the output grid                                       #
# - mlon: (float)                                                             #
#     Mean longitude for the output grid                                      #
# - L0: (float)                                                               #
#     Total longitude for the output                                          #
###############################################################################

N0 = 512
Nlim = 20
giveboundary = False
mlat = 37.
mlon = -57.
L0 = 1600000


###############################################################################
#                            SAVING PARAMETERS                                #
###############################################################################
# - path2save: (str)                                                          # 
#     Path where the data will be saved                                       #
# - savename: (str)                                                           #
#     Saving name                                                             #
###############################################################################

path2save = '/scratch/cnt0024/hmg2840/emartin/DATA/E' + region + '/'
savename = filename[:-3] + '_' + str(N) + 'x' + str(N) + '.nc'


###############################################################################
#                            SPLITING PARAMETERS                              #
###############################################################################
# - split: (bool)                                                             #
#     True for split the data in sub-boxes                                    #
# - Nbox: (int)                                                               #
#     Square root of the number of sub-boxes                                  #
###############################################################################

split = True
Nbox = 4

###############################################################################
#                                3D PARAMETERS                                #
###############################################################################
# - NL: (int)                                                                 #
#     Number of vertical layers to be taken. Set 0 for 2D data                #
# - Lind: (int)                                                               #
#     Index of the layers. First layer NL*Lind+1, last layer NL*(Lind+1)      # 
# - depname: (str)                                                            #
#     Name of the depths variable to be loaded                                #
###############################################################################

NLs = [30]
Lind = None
depname = 'deptht'
