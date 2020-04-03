import dask
import numpy as np
import xarray as xr
from msqg_tools.opends import load_1file
from msqg_tools.breakds import breakds
from msqg_tools.tools import int2iterable, split_iterable


def mask_main(filename, savename, latname, lonname,
              Nproc=1, ind=None, Nb=None):
    """
    Creates a mask of are values for a file or a set of splitted files.
    If one file is used this can be automatically splitted using ind_out.

    Parameters
    ----------
    filename : str
        Name of the file to be open.
    savename : str
        Name of the file to be saved.
    latname : str
        Name of the latitude variable.
    lonname : str
        Name of the longitude variable.
    Nproc : int, optional
        If bigger than 1 will run in parallel. The default is 1.
    ind : tuple, optional
        If the file(s) to be loaded come(s) from a partition from breakds
        a tuple with the index must be provided (Z, Y, X). Where X, Y, Z
        are the respective index in each dimension (floats or array like).
        In that case the loaded data will be appended.
        The default is None.
    Nb : tuple of 3 int, optional
        Number of partitions to be made in the z, y and x axis.
        Only used if ind is None and Nb not None. The default is None.

    Returns
    -------
    None.
    """
    if ind is None:
        mask_1file(filename, savename, latname, lonname, ind, Nb)
    else:
        def mask_kji(kji):
            k, j, i = kji
            fname = filename + '_' + str(k) + '_' + str(j) + '_' + str(i)
            fsave = savename + '_' + str(k) + '_' + str(j) + '_' + str(i)
            mask_1file(fname, fsave, latname, lonname, ind, None)
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
                    run_paral = dask.delayed(mask_kji)(kji)
                    output.append(run_paral)
                total = dask.delayed(sum)(output)
                total.compute()

        # Run in series
        else:
            print("Processing {} files".format(totl))
            for i, kji_ in enumerate(kji_com):
                print("\t{:.2f}%".format(100.*i/totl))
                mask_kji(kji_)


def mask_1file(filename, savename, latname, lonname, ind, Nb):
    """
    Computes the mask of areas for a given file.
    Check the documentation of mask_main for more information.
    """

    #############
    # LOAD DATA #
    #############

    _, lats, lons, _, _ = load_1file(filename, [], latname, lonname,
                                     None, None)
    latm = lats.copy()
    lonm = lats.copy()
    nanvalues = np.logical_and(latm == 0, lonm == 0)
    latm[nanvalues] = np.nan
    lonm[nanvalues] = np.nan

    dlat = np.gradient(latm)
    dlon = np.gradient(lonm)
    dx = np.sqrt((111000*dlon[1]*np.cos(np.deg2rad(latm)))**2
                 + 111000*dlat[1]**2)
    dy = np.sqrt((111000*dlon[0]*np.cos(np.deg2rad(latm)))**2
                 + 111000*dlat[0]**2)

    dx[np.isnan(dx)] = 0.
    dy[np.isnan(dy)] = 0.
    mask = dx * dy

    if Nb is None:
        # Save as the original file
        ds = xr.Dataset({lonname: (('y', 'x'), lons),
                         latname: (('y', 'x'), lats),
                         'mask': (('y', 'x'), mask)})
        ds.to_netcdf(savename+'.nc')
    else:
        # Save splitted data
        breakds(savename, ['mask'], latname, lonname,
                Nb=Nb, passvalues=([mask], lats, lons, None, None))
