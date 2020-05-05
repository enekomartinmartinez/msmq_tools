import numpy as np
import xarray as xr
from msqg_tools.tools import int2iterable


def load_main(filename, varnames, latname, lonname,
              depname=None, timname=None, ind=None):
    """
    Loading data function. Lets load data from 1 file and from breakds
    splitted files if ind is provided.

    Parameters
    ----------
    filename : str
        Name of the file to be open.
    varnames : list of str
        Name of the vars to be extracted and saved in the splitted files.
    latname : str
        Name of the latitude variable.
    lonname : str
        Name of the longitude variable.
    depname : str, optional
        Name of the depth variable. The default is None.
    timname : str, optional
        Name of the time variable. The default is None.
    ind : tuple, optional
        If the file(s) to be loaded come(s) from a partition from breakds
        a tuple with the index must be provided (Z, Y, X). Where X, Y, Z
        are the respective index in each dimension (floats or array like).
        In that case the loaded data will be appended.
        The default is None.

    Returns
    -------
    vars, lat, lon, tim, dep: tuple
        Tuple of the list of variables, latitudes, longitudes,
        times (if timname is not None), depths (if depname is not None)
    """

    if ind is None:
        return load_1file(filename, varnames, latname, lonname,
                          depname, timname)
    else:
        return load_split(filename, varnames, latname, lonname,
                          depname, timname, ind)


def load_1file(filename, varnames, latname, lonname,
               depname, timname):
    """
    Load data from 1 file.
    Check the documentation of load_main for more information.
    """

    vars_in = []
    dep_in = None
    tim_in = None

    # Read values
    with xr.open_dataset(filename+'.nc') as data:
        for varn in varnames:
            vars_in.append(data[varn].values)
        lat_in = data[latname].values
        lon_in = data[lonname].values
        if depname is not None:
            dep_in = data[depname].values
        if timname is not None:
            tim_in = data[timname].values

    if len(lat_in.shape) == 1:
        lon_in, lat_in = np.meshgrid(lon_in, lat_in)

    return vars_in, lat_in, lon_in, tim_in, dep_in


def load_split(filename, varnames, latname, lonname,
               depname, timname, ind):
    """
    Load splitted data.
    Check the documentation of load_main for more information.
    """

    # Transform the floats to iterables
    indk = int2iterable(ind[0])
    indj = int2iterable(ind[1])
    indi = int2iterable(ind[2])

    tim_in = None
    nvars = len(varnames)

    # Loop appending the values
    vars_k = [None for v in range(nvars)]
    dep_k = None
    for k in indk:
        vars_j = [None for var in varnames]
        lat_j, lon_j = None, None
        for j in indj:
            vars_i = [None for var in varnames]
            lat_i, lon_i = None, None
            for i in indi:
                filenamekji = filename+'_'+str(k)+'_'+str(j)+'_'+str(i)
                with xr.open_dataset(filenamekji+'.nc') as data:
                    for v in range(nvars):
                        if vars_i[v] is None:
                            vars_i[v] = data[varnames[v]].values
                        else:
                            vars_i[v] = np.append(vars_i[v],
                                                  data[varnames[v]].values,
                                                  axis=-1)
                    if lat_i is None:
                        lat_i = data[latname].values
                        lon_i = data[lonname].values
                    else:
                        lat_i = np.append(lat_i, data[latname].values, axis=-1)
                        lon_i = np.append(lon_i, data[lonname].values, axis=-1)
                    if depname is not None:
                        dep_in = data[depname].values
                    if timname is not None:
                        tim_in = data[timname].values
            for v in range(nvars):
                if vars_j[v] is None:
                    vars_j[v] = vars_i[v]
                else:
                    vars_j[v] = np.append(vars_j[v], vars_i[v], axis=-2)
            if lat_j is None:
                lat_j = lat_i
                lon_j = lon_i
            else:
                lat_j = np.append(lat_j, lat_i, axis=-2)
                lon_j = np.append(lon_j, lon_i, axis=-2)
        for v in range(nvars):
            if len(vars_j[v].shape) == 3 or vars_k[v] is None:
                vars_k[v] = vars_j[v]
            else:
                vars_k[v] = np.append(vars_k[v], vars_j[v], axis=-3)
        if depname is not None:
            if dep_k is None:
                dep_k = dep_in
            else:
                dep_k = np.append(dep_k, dep_in)

    return vars_k, lat_j, lon_j, tim_in, dep_k
