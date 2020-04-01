import xarray as xr
from opends import load_1file
from tools import create_partition


def breakds(filename, varnames, latname, lonname,
            Nb=(1, 1, 1), passvalues=None,
            depname=None, timname=None):
    """
    Breaking function to split a big dataset in smaller one.
    From file filename.nc will create filename_Z_Y_X.nc, where Z, Y, X
    are the partition number in each respective axis.
    It is also possible to make the partition passing the values.

    Parameters
    ----------
    filename : str
        Name of the original file.
    varnames : list of str
        Name of the vars to be extracted and saved in the splitted files.
    latname : str
        Name of the latitude variable.
    lonname : str
        Name of the longitude variable.
    Nb : tuple of 3 int, optional
        Number of partitions to be made in the z, y and x axis.
        The default is (1, 1, 1).
    passvalues: tuple
        Tuple variables, latitudes, longitudes, times and depths.
        If None will read the data from the filename.
        The default is None.
    depname : str, optional
        Name of the depth variable. The default is None.
    timname : str, optional
        Name of the time variable. The default is None.

    Returns
    -------
    None.

    """

    if passvalues is None:
        #############
        # LOAD DATA #
        #############
        print("Loading data")
    
        vars_in, lat, lon, tim, dep = load_1file(filename, varnames,
                                                 latname, lonname,
                                                 depname, timname)
    else:
        vars_in, lat, lon, tim, dep = passvalues

    svar = vars_in.shape
    Nk = create_partition(Nb[0], svar[1])
    Nj = create_partition(Nb[1], svar[2])
    Ni = create_partition(Nb[2], svar[3])

    #############
    # SAVE DATA #
    #############

    print("Saving data")
    for k in range(Nb[0]):
        for j in range(Nb[1]):
            for i in range(Nb[2]):
                name = filename+'_'+str(k)+'_'+str(j)+'_'+str(i)+'.nc'
                ds = {lonname: (('y', 'x'),
                                lon[Nj[j]:Nj[j+1],
                                    Ni[i]:Ni[i+1]]),
                      latname: (('y', 'x'),
                                lat[Nj[j]:Nj[j+1],
                                    Ni[i]:Ni[i+1]])}
                for v in range(len(varnames)):
                    if len(vars_in[v].shape) == 4:
                        ds[varnames[v]] = (('t', 'z', 'y', 'x'),
                                           vars_in[v][:
                                                      Nk[j]:Nk[j+1],
                                                      Nj[j]:Nj[j+1],
                                                      Ni[i]:Ni[i+1]])
                    elif len(vars_in[v].shape) == 3:
                        ds[varnames[v]] = (('t', 'y', 'x'),
                                           vars_in[v][:
                                                      Nj[j]:Nj[j+1],
                                                      Ni[i]:Ni[i+1]])
                    elif len(vars_in[v].shape) == 2:
                        ds[varnames[v]] = (('y', 'x'),
                                           vars_in[v][Nj[j]:Nj[j+1],
                                                      Ni[i]:Ni[i+1]])
                if depname is not None:
                    ds[depname] = (('z'), dep)
                if timname is not None:
                    ds[timname] = (('t'), tim)
                ds = xr.Dataset(ds)
                ds.to_netcdf(name)
