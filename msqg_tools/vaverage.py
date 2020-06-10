import dask
import numpy as np
import xarray as xr
from msqg_tools.opends import load_1file
from msqg_tools.tools import int2iterable, split_iterable


def vaverage_main(filename, savename, varname, latname, lonname,
                  depname=None, timname=None, interval=None,
                  Nproc=1, ind=None):
    """
    Creates a mask of are values for a file or a set of splitted files.
    If one file is used this can be automatically splitted using ind_out.

    Parameters
    ----------
    filename : str
        Name of the file to be open.
    maskname : str
        Name of the mask file to compute the average.
    savename : str
        Name of the file to be saved.
    varname : str
        Name of the var to be averaged.
    latname : str
        Name of the latitude variable.
    lonname : str
        Name of the longitude variable.
    depname : str, optional
        Name of the depth variable. The default is None.
    timname : str, optional
        Name of the time variable. The default is None.
    Nproc : int, optional
        If bigger than 1 will run in parallel. The default is 1.
    ind : tuple, optional
        If the file(s) to be loaded come(s) from a partition from breakds
        a tuple with the index must be provided (Z, Y, X). Where X, Y, Z
        are the respective index in each dimension (floats or array like).
        The default is None.

    Returns
    -------
    None.
    """

    if ind is None:
        vaverage_1file(filename, savename, varname, latname, lonname,
                       depname, timname, interval)
    # Get data from splitted files
    else:

        def vav_kji(kji):
            k, j, i = kji
            fname = filename+'_'+str(k)+'_'+str(j)+'_'+str(i)
            fsave = savename+'_'+str(k)+'_'+str(j)+'_'+str(i)
            vaverage_1file(fname, fsave, varname, latname, lonname,
                           depname, timname, interval)
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
                    run_paral = dask.delayed(vav_kji)(kji)
                    output.append(run_paral)
                total = dask.delayed(sum)(output)
                total.compute()

        # Run in series
        else:
            print("Processing {} files".format(totl))
            for i, kji_ in enumerate(kji_com):
                print("\t{:.2f}%".format(100.*i/totl))
                vav_kji(kji_)


def vaverage_1file(filename, savename, varname, latname, lonname,
                   depname, timname, interval):
    """
    Computes the mask of areas for a given file.
    Check the documentation of mask_main for more information.
    """

    #############
    # LOAD DATA #
    #############

    [var], lats, lons, tim, dep = load_1file(filename, [varname],
                                             latname, lonname,
                                             depname, timname)

    if interval is None:
        interval = (-1, 1e9)

    ind = np.logical_and(dep >= interval[0], dep <= interval[1])

    sh = var.shape
    h = np.gradient(dep)[ind][None, :, None, None]
    h = np.tile(h , (sh[0], 1, sh[2], sh[3]))
    var = var[:, ind]
    isnan = np.isnan(var)
    h[isnan] = 0
    var[isnan] = 0
    av_var = np.sum(h * var, axis=1) / np.sum(h, axis=1)

    #############
    # SAVE DATA #
    #############

    ds = {lonname: (('y', 'x'), lons),
          latname: (('y', 'x'), lats),
          varname: (('t', 'y', 'x'), av_var)}

    if timname is not None:
        ds[timname] = (('t'), tim)

    ds = xr.Dataset(ds)
    ds.to_netcdf(savename+'.nc')
