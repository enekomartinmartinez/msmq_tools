import dask
import numpy as np
import xarray as xr
from msqg_tools.opends import load_1file
from msqg_tools.tools import int2iterable, split_iterable


def average_main(filename, maskname, varname, latname, lonname,
                 depname=None, timname=None, gridval=None,
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
        f_var, f_lat, f_lon, weight, tim, dep =\
            average_1file(filename, maskname, varname, latname,
                          lonname, depname, timname, gridval)
        f_var = f_var/weight
        f_lat = f_lat/weight
        f_lon = f_lon/weight

    else:
        def avg_kji(kji):
            k, j, i = kji
            fname = filename + '_' + str(k) + '_' + str(j) + '_' + str(i)
            mname = maskname + '_' + str(k) + '_' + str(j) + '_' + str(i)
            outs.append(average_1file(fname, mname, varname,
                                      latname, lonname, depname,
                                      timname, gridval))
            return 1

        # Get iterables for the 3 index and call combinations
        indk = int2iterable(ind[0])
        indj = int2iterable(ind[1])
        indi = int2iterable(ind[2])

        dep = np.array([])
        f_var = np.array([])
        for k in indk:
            outs = []
            kji_com = [(k, j, i) for j in indj for i in indi]
            totl = len(kji_com)

            # Run in parallel
            if Nproc > 1:
                kji_com = split_iterable(kji_com, Nproc)
                print("Processing {} files with {} cores".format(totl,
                                                                 Nproc))
                totl = len(kji_com)
                for i, kji_ in enumerate(kji_com):
                    print("\t{:.2f}%".format(100.*i*(k+1)/totl))
                    output = []
                    for kji in kji_:
                        run_paral = dask.delayed(avg_kji)(kji)
                        output.append(run_paral)
                    total = dask.delayed(sum)(output)
                    total.compute()

            # Run in series
            else:
                print("Processing {} files".format(totl))
                for i, kji_ in enumerate(kji_com):
                    print("\t{:.2f}%".format(100.*i*(k+1)/totl))
                    avg_kji(kji_)

            tav_val, tav_lon, tav_lat, tweight = np.zeros_like(outs[0][0]), 0., 0., 0.
            for av_val, av_lat, av_lon, weight, _, _ in outs:
                tav_val += av_val
                tav_lat += av_lat
                tav_lon += av_lon
                tweight += weight
            dep = np.append(dep, outs[0][5])
            if len(f_var.shape) == 2:
                f_var = np.append(f_var, tav_val/tweight, axis=-1)
            elif f_var.shape[0] != 0:
                f_var = np.append(f_var, tav_val/tweight)
            else:
                f_var = tav_val/tweight
            f_lat = tav_lat/tweight
            f_lon = tav_lon/tweight

        tim = outs[0][4]

        #############
        # SAVE DATA #
        #############

        ds = {lonname: ((), f_lon),
              latname: ((), f_lat)}

        if timname is not None:
            ds[timname] = (('t'), tim)
        if depname is not None:
            ds[depname] = (('z'), dep)

        if len(f_var.shape) == 2:
            ds[varname] = (('t', 'z'), f_var)
        else:
            ds[varname] = (('t'), f_var)

        ds = xr.Dataset(ds)
        ds.to_netcdf(filename+'_mean.nc')


def average_1file(filename, maskname, varname, latname, lonname,
                  depname, timname, gridval):
    """
    Computes the mask of areas for a given file.
    Check the documentation of mask_main for more information.
    """

    #############
    # LOAD DATA #
    #############

    [mask], latm, lonm, _, _ = load_1file(maskname, ['mask'],
                                          latname, lonname,
                                          None, None)

    [var], lats, lons, tim, dep = load_1file(filename, [varname],
                                             latname, lonname,
                                             depname, timname)

    lons, lonm = lons % 360, lonm % 360
    gridval[0], gridval[1] = gridval[0] % 360, gridval[1] % 360
    if np.any(lats != latm) or np.any(lons != lonm):
        raise ValueError("The latitudes-longitudes field does not match")

    if gridval is not None:
        indyx = np.logical_or(
            np.logical_or(lonm < gridval[0], lonm > gridval[1]),
            np.logical_or(latm < gridval[2], latm > gridval[3]))
        mask[indyx] == 0

    av_lon = np.nansum(mask*lons)
    av_lat = np.nansum(mask*lats)

    if len(var.shape) == 4:
        mask[np.isnan(var[0, 0])] = 0
        mask = mask[np.newaxis, np.newaxis, :, :]
    elif len(var.shape) == 3:
        mask[np.isnan(var[0])] = 0
        mask = mask[np.newaxis, :, :]
    elif len(var.shape) == 2:
        mask[np.isnan(var)] = 0

    av = np.nansum(mask*var, axis=(-1, -2))
    return av, av_lat, av_lon, np.sum(mask), tim, dep
