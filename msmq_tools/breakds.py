import xarray as xr
from opends import load_1file
from tools import create_partition


def breakds(filename, varnames, latname, lonname,
            Nbx=1, Nby=1, Nbz=1,
            depname=None, timname=None):
    """
    Breaking function to split a big dataset in smaller one.
    From file filename.nc will create filename_Z_Y_X.nc, where Z, Y, X
    are the partition number in each respective axis.

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
    Nbx : int, optional
        Number of partitions to be made in the x axis. The default is 1.
    Nby : int, optional
        Number of partitions to be made in the y axis. The default is 1.
    Nbz : int, optional
        Number of partitions to be made in the z axis. The default is 1.
    depname : str, optional
        Name of the depth variable. The default is None.
    timname : str, optional
        Name of the time variable. The default is None.

    Returns
    -------
    None.

    """

    #############
    # LOAD DATA #
    #############

    print("Loading data")

    vars_in, lat, lon, tim, dep = load_1file(filename, varnames,
                                             latname, lonname,
                                             depname, timname)

    svar = vars_in.shape
    Nk = create_partition(Nbz, svar[1])
    Nj = create_partition(Nby, svar[2])
    Ni = create_partition(Nbx, svar[3])

    #############
    # SAVE DATA #
    #############

    print("Saving data")
    for k in range(Nbz):
        for j in range(Nby):
            for i in range(Nbx):
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
                    else:
                        ds[varnames[v]] = (('t', 'y', 'x'),
                                           vars_in[v][:
                                                      Nj[j]:Nj[j+1],
                                                      Ni[i]:Ni[i+1]])
                if depname is not None and depname != '':
                    ds[depname] = (('z'), dep)
                if timname is not None and timname != '':
                    ds[timname] = (('t'), tim)
                ds = xr.Dataset(ds)
                ds.to_netcdf(name)
