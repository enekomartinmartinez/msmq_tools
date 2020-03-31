import numpy as np
import xarray as xr
from seawater.eos80 import pres, pden
from opends import load_main
from tools import int2iterable


def den_main(filename_tem, filename_sal, filename_mask, savename,
             temname, salname, depname, denname, latname, lonname,
             pressure_lvl=False, max_dep=None, mlat=None, parallel=False,
             timname=None, ind=None, tb=None, zb=None, yb=None, xb=None):
    """
    Compute density profile of 1 file or spplitted files if ind is provided.
    Save the file as the input format and save an extra file with the mean
    profile called savename_mean.nc.

    Parameters
    ----------
    filename_tem : str
        Name of the temperature data file.
    filename_sal : str
        Name of the salinity data file.
    filename_mask : str
        Name of the weights mask data file. created with weight.py
    savename : str
        Name to the saving file.
    temname : str
        Name of the temperature variable.
    temname : str
        Name of the salinity variable.
    latname : str
        Name of the latitude variable.
    lonname : str
        Name of the longitude variable.
    pressure_lvl : Bool, optional
        True if the depth variable is the pressure level.
        The default is False.
    max_dep : float, optional
        Maximum depth to be used when computing the profiles.
        The default is None.
    mlat : float, optional
        If provided, mean latitude is used to compute pressure levels.
        The default is None.
    parallel : bool, optional
        Running in parallel option. The default is False.
    timname : str, optional
        Name of the time variable. The default is None.
    ind : tuple, optional
        If the file or files to be loaded come from a partition from breakds
        a tuple with the index must be provided (Z, Y, X). Where X, Y, Z
        are the respective index in each dimension (floats or array like).
        In that case the loaded data will be appended.
    tb : float or array like, optional
        Subset to be extracted in the time dimension. The default is None.
    zb : float or array like, optional
        Subset to be extracted in the z dimension. The default is None.
    yb : float or array like, optional
        Subset to be extracted in the y dimension. The default is None.
    xb : float or array like, optional
        Subset to be extracted in the x dimension. The default is None.

    Returns
    -------
    None.

    """

    # Get data from 1 file
    if ind is None:
        mp = [den_1file(filename_tem, filename_sal, filename_mask, savename,
                        temname, salname, depname, denname, latname, lonname,
                        pressure_lvl, max_dep, mlat, timname, tb, zb, yb, xb)]

    # Get data from splitted files
    else:
        mp = []

        def den_kji(kji):
            k, j, i = kji
            fname_tem = filename_tem+'_'+str(k)+'_'+str(j)+'_'+str(i)
            fname_sal = filename_sal+'_'+str(k)+'_'+str(j)+'_'+str(i)
            fname_mask = filename_mask+'_'+str(k)+'_'+str(j)+'_'+str(i)
            fsave_den = savename+'_'+str(k)+'_'+str(j)+'_'+str(i)
            mp.append(den_1file(fname_tem, fname_sal, fname_mask, fsave_den,
                                temname, salname, depname, denname,
                                latname, lonname, pressure_lvl,
                                max_dep, mlat, timname, tb, zb, yb, xb))
            return 1

        # Get iterables for the 3 index and call combinations
        indk = int2iterable(ind[0])
        indj = int2iterable(ind[1])
        indi = int2iterable(ind[2])

        kji_com = [(k, j, i) for k in indk for j in indj for i in indi]

        # Run in parallel
        if parallel:
            # TO BE DEVELOPED
            pass
        # Run in series
        else:
            for kji_ in kji_com:
                den_kji(kji_)

    ################################
    # COMPUTE AND SAVE MEAN VALUES #
    ################################

    Den, Lat, Lon, Wei = np.zeros_like(mp[0][0]), 0, 0, 0
    for den, lat, lon, dep, tim, weight in mp:
        Den += den
        Lat += lat
        Lon *= lon
        Wei += weight
    Den /= Wei
    Lat /= Wei
    Lon /= Wei

    ds = {lonname: ((), Lon),
          latname: ((), Lat),
          depname: (('z'), dep),
          denname: (('t', 'z'), Den)}

    if timname is not None:
        ds[timname] = (('t'), tim)

    ds = xr.Dataset(ds)
    ds.to_netcdf(savename+'_mean.nc')


def den_1file(filename_tem, filename_sal, filename_mask, savename, temname,
              salname, depname, denname, latname, lonname, pressure_lvl,
              max_dep, mlat, timname, tb, zb, yb, xb):
    """
    Computes the density profile from a given file.
    Check the documentation of den_main for more information.
    """

    #############
    # LOAD DATA #
    #############

    if filename_tem == filename_sal:
        # Launch reading routine for 1 file
        [tem, sal], lats, lons, tim, deps = load_main(filename_tem,
                                                      [temname, salname],
                                                      latname, lonname,
                                                      [1, 1], depname,
                                                      timname,
                                                      tb=tb, zb=zb,
                                                      yb=yb, xb=xb)

    else:
        # Launch reading routine for 2 different files
        [tem], _, _, _, _ = load_main(filename_tem, [temname],
                                      latname, lonname,
                                      [1], depname, timname,
                                      tb=tb, zb=zb, yb=yb, xb=xb)
        [sal], lat, lon, tim, deps = load_main(filename_sal, [salname],
                                               latname, lonname,
                                               [1], depname, timname,
                                               tb=tb, zb=zb, yb=yb, xb=xb)

    # Remove data from very high depth
    if max_dep is not None:
        ind = (deps < max_dep)
        sal, tem, deps = sal[:, ind, :, :], tem[:, ind, :, :], deps[ind]

    pdens = np.empty_like(sal)
    dim = lats.shape

    ######################
    # GET DENSITY VALUES #
    ######################

    # Depth variable is already a pressure level
    if pressure_lvl:
        for j in range(dim[0]):
            for i in range(dim[1]):
                pdens[:, :, i, j] = pden(sal[:, :, i, j],
                                         tem[:, :, i, j],
                                         deps)
    # Compute the pressure levels with a mean latitude value
    elif mlat is not None:
        pre = pres(deps, mlat)
        for j in range(dim[0]):
            for i in range(dim[1]):
                pdens[:, :, i, j] = pden(sal[:, :, i, j],
                                         tem[:, :, i, j],
                                         pre)
        del pre
    # Compute pressure levels with all the latitudes
    else:
        for j in range(dim[0]):
            for i in range(dim[1]):
                pdens[:, :, i, j] = pden(sal[:, :, i, j],
                                         tem[:, :, i, j],
                                         pres(deps, lats[i, j]))

    #############
    # SAVE DATA #
    #############

    ds = {lonname: (('y', 'x'), lon),
          latname: (('y', 'x'), lat),
          depname: (('z'), deps),
          denname: (('t', 'z', 'y', 'x'), pdens)}

    if timname is not None:
        ds[timname] = (('t'), tim)

    ds = xr.Dataset(ds)
    ds.to_netcdf(savename+'.nc')
    del ds

    #############
    # LOAD MASK #
    #############

    [mask], latm, lonm, _, _ = load_main(filename_mask, ['mask'],
                                         latname, lonname, [1, 1],
                                         None, None, tb=tb, zb=zb,
                                         yb=yb, xb=xb)

    if np.any(latm != lats) or np.any(lonm != lons):
        raise ValueError("The mask doesn't match the data")

    ########################
    # COMPUTE WEIGHTED SUM #
    ########################

    # If there is any nan value in a vertical column set mask=0
    nanid = np.any(np.isnan(pdens), axis=(0, 1))
    mask[nanid] = 0
    mlat = np.sum(mask*latm)
    mlon = np.sum(mask*lonm)
    mask = mask[np.newaxis, np.newaxis, :, :]
    mden = np.sum(mask*pdens, axis=(2, 3))
    mmask = np.sum(mask)
    return mden, mlat, mlon, deps, tim, mmask
