import numpy as np
import xarray as xr
from msqg_tools.opends import load_1file


def genini_main(filename, varnames, latname, lonname, mlat, mlon,
                L0, N0=512, Nlim=0):

    #############
    # LOAD DATA #
    #############
    file_in = filename + '_' + str(N0-2*Nlim) + 'x'\
              + str(N0-2*Nlim) + '_equidis'
    Nlim = Nlim + 10

    vars_in, _, _, _, _ = load_1file(file_in, varnames,
                                     latname, lonname,
                                     None, None)

    ##############
    # CREATE DIM #
    ##############

    x = np.linspace(-L0/2, L0/2, N0)
    X, Y = np.meshgrid(x, x)
    lat_out = mlat + Y/111000
    lon_out = mlon + X/111000/np.cos(np.deg2rad(lat_out))
    vars_out = [np.empty((1, N0, N0)) for var in vars_in]

    #####################
    # CREATE BOUNDARIES #
    #####################

    lin1 = np.linspace(0, 1, Nlim, endpoint=False)
    lin2 = np.linspace(1, 0, Nlim, endpoint=False)
    for i in range(len(vars_out)):
        vars_out[i][:, Nlim:(N0-Nlim), Nlim:(N0-Nlim)] = vars_in[i][:1, 10:-10, 10:-10]
        vars_out[i][:, :Nlim, :] = vars_out[i][:, Nlim, :][:, np.newaxis, :]\
                                   * lin1[np.newaxis, :, np.newaxis]
        vars_out[i][:, :, :Nlim] = vars_out[i][:, :, Nlim][:, :, np.newaxis]\
                                   * lin1[np.newaxis, np.newaxis, :]
        vars_out[i][:, -Nlim:, :] = vars_out[i][:, N0-Nlim-1, :][:, np.newaxis, :]\
                                    * lin2[np.newaxis, :, np.newaxis]
        vars_out[i][:, :, -Nlim:] = vars_out[i][:, :, N0-Nlim-1][:, :, np.newaxis]\
                                    * lin2[np.newaxis, np.newaxis, :]

    #############
    # SAVE DATA #
    #############

    file_out = filename + '_' + str(N0) + 'x'\
               + str(N0) + '_ini'

    ds = {lonname: (('y', 'x'), lon_out),
          latname: (('y', 'x'), lat_out)}

    for var, varn in zip(vars_out, varnames):
        ds[varn] = (('t', 'y', 'x'), var)

    ds = xr.Dataset(ds)
    ds.to_netcdf(file_out+'.nc')
