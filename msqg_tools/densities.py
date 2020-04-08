import numpy as np
import xarray as xr
import dask
from seawater.eos80 import pres, pden
from msqg_tools.opends import load_main
from msqg_tools.tools import int2iterable, split_iterable


def den_main(filename_tem, filename_sal, savename,
             temname, salname, depname, denname, latname, lonname,
             pressure_lvl=False, mlat=None, Nproc=1,
             timname=None, ind=None):
    """
    Computes the density profile of a file or a set splitted files.
    Saves the file as the input format.

    Parameters
    ----------
    filename_tem : str
        Name of the temperature data file.
    filename_sal : str
        Name of the salinity data file.
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
    mlat : float, optional
        If provided, mean latitude is used to compute pressure levels.
        The default is None.
    Nproc : int, optional
        If bigger than 1 will run in parallel. The default is 1.
    timname : str, optional
        Name of the time variable. The default is None.
    ind : tuple, optional
        If the file or files to be loaded come from a partition from breakds
        a tuple with the index must be provided (Z, Y, X). Where X, Y, Z
        are the respective index in each dimension (floats or array like).
        In that case the loaded data will be appended.

    Returns
    -------
    None.

    """

    # Get data from 1 file
    if ind is None:
        mp = [den_1file(filename_tem, filename_sal, savename,
                        temname, salname, depname,
                        denname, latname, lonname,
                        pressure_lvl, mlat, timname)]

    # Get data from splitted files
    else:
        mp = []

        def den_kji(kji):
            k, j, i = kji
            fname_tem = filename_tem+'_'+str(k)+'_'+str(j)+'_'+str(i)
            fname_sal = filename_sal+'_'+str(k)+'_'+str(j)+'_'+str(i)
            fsave_den = savename+'_'+str(k)+'_'+str(j)+'_'+str(i)
            mp.append(den_1file(fname_tem, fname_sal, fsave_den,
                                temname, salname, depname, denname,
                                latname, lonname, pressure_lvl,
                                mlat, timname))
            return 1

        # Get iterables for the 3 index and call combinations
        indk = int2iterable(ind[0])
        indj = int2iterable(ind[1])
        indi = int2iterable(ind[2])

        kji_com = [(k, j, i) for k in indk for j in indj for i in indi]
        totl = len(kji_com)

        # Run in parallel
        if Nproc > 1:
            kji_com = split_iterable(kji_com, Nproc)
            print("Processing {} files with {} cores".format(totl, Nproc))
            totl = len(kji_com)
            for i, kji_ in enumerate(kji_com):
                print("\t{:.2f}%".format(100.*i/totl))
                output = []
                for kji in kji_:
                    run_paral = dask.delayed(den_kji)(kji)
                    output.append(run_paral)
                total = dask.delayed(sum)(output)
                total.compute()

        # Run in series
        else:
            print("Processing {} files".format(totl))
            for i, kji_ in enumerate(kji_com):
                print("\t{:.2f}%".format(100.*i/totl))
                den_kji(kji_)


def den_1file(filename_tem, filename_sal, savename, temname,
              salname, depname, denname, latname, lonname, pressure_lvl,
              mlat, timname):
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
                                                      depname, timname)

    else:
        # Launch reading routine for 2 different files
        [tem], _, _, _, _ = load_main(filename_tem, [temname],
                                      latname, lonname,
                                      depname, timname)
        [sal], lats, lons, tim, deps = load_main(filename_sal, [salname],
                                                 latname, lonname,
                                                 depname, timname)

    pdens = np.empty_like(sal)
    dim = lats.shape
    index = np.logical_and(sal == 0, tem == 0)
    sal[index], tem[index] = np.nan, np.nan
    index = np.logical_and(lats == 0, lons == 0)
    lats[index], lons[index] = np.nan, np.nan

    ######################
    # GET DENSITY VALUES #
    ######################

    # Depth variable is already a pressure level
    if pressure_lvl:
        for j in range(dim[0]):
            for i in range(dim[1]):
                for t in range(sal.shape[0]):
                    pdens[t, :, j, i] = pden(sal[t, :, j, i],
                                             tem[t, :, j, i],
                                             deps)
    # Compute the pressure levels with a mean latitude value
    elif mlat is not None:
        pre = pres(deps, mlat)
        for j in range(dim[0]):
            for i in range(dim[1]):
                for t in range(sal.shape[0]):
                    pdens[t, :, j, i] = pden(sal[t, :, j, i],
                                             tem[t, :, j, i],
                                             pre)
        del pre
    # Compute pressure levels with all the latitudes
    else:
        for j in range(dim[0]):
            for i in range(dim[1]):
                pre = pres(deps, lats[j, i])
                for t in range(sal.shape[0]):
                    pdens[t, :, j, i] = pden(sal[t, :, j, i],
                                             tem[t, :, j, i],
                                             pre)

    #############
    # SAVE DATA #
    #############

    ds = {lonname: (('y', 'x'), lons),
          latname: (('y', 'x'), lats),
          depname: (('z'), deps),
          denname: (('t', 'z', 'y', 'x'), pdens)}

    if timname is not None:
        ds[timname] = (('t'), tim)

    ds = xr.Dataset(ds)
    ds.to_netcdf(savename+'.nc')
