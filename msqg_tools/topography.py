import numpy as np
import xarray as xr
from msqg_tools.opends import load_main


def topo_main(filename, savename, varname, topname,
              latname, lonname, depname, timname):
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

    [bathy], lat, lon, tim, dep = load_main(filename, [varname], latname,
                                            lonname, depname, timname)

    sh = bathy.shape
    if len(sh) == 2:
        bathy = bathy[None, :, :]
        sh = bathy.shape


    topo = np.empty_like(bathy)
    for i in range(sh[1]):
        for j in range(sh[2]):
            topo[:, i, j] = dep[int(bathy[0, i, j])]

    print("Main depth: ", np.mean(topo))
    ds = xr.Dataset({timname:(('t'), tim),
                     lonname: (('y', 'x'), lon),
                     latname: (('y', 'x'), lat),
                     topname: (('t','y', 'x'), topo)})
    ds.to_netcdf(savename+'.nc')
