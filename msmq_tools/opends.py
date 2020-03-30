import numpy as np
import xarray as xr


def load_main(filename, varnames, latname, lonname,
              NL, depname=None, timname=None, ind=None,
              tb=(None, None), zb=(None, None),
              yb=(None, None), xb=(None, None)):

    if ind is None:
        return load_1file(filename, varnames, latname, lonname,
                          depname, timname, NL, tb, zb, yb, xb)
    else:
        return load_split(filename, varnames, latname, lonname,
                          depname, timname, NL, ind)


def load_1file(filename, varnames, latname, lonname,
               depname, timname, NL, tb, zb, yb, xb):

    vars_in = []
    dep_in = None
    tim_in = None

    with xr.open_dataset(filename+'.nc') as data:
        for i in range(len(varnames)):
            if NL[i] > 0:
                vars_in.append(data[varnames[i]].values[tb[0]:tb[1],
                                                        zb[0]:zb[1],
                                                        yb[0]:yb[1],
                                                        xb[0]:xb[1]])
            else:
                vars_in.append(data[varnames[i]].values[tb[0]:tb[1],
                                                        yb[0]:yb[1],
                                                        xb[0]:xb[1]])
        lat_in = data[latname].values[yb[0]:yb[1],
                                      xb[0]:xb[1]]
        lon_in = data[lonname].values[yb[0]:yb[1],
                                      xb[0]:xb[1]]
        if depname is not None:
            dep_in = data[depname].values[zb[0]:zb[1]]
        if timname is not None:
            tim_in = data[timname].values[tb[0]:tb[1]]

    return vars_in, lat_in, lon_in, tim_in, dep_in


def load_split(filename, varnames, latname, lonname,
               NL, depname, timname, ind):

    def int2iterable(val):
        if type(val) is int:
            return [val]
        else:
            return val

    indk = int2iterable(ind[0])
    indj = int2iterable(ind[1])
    indi = int2iterable(ind[2])

    tim_in = None

    nvars = len(varnames)
    vars_k = [np.array([]) for v in range(nvars)]
    dep_k = np.array([])
    for k in indk:
        vars_j = [np.array([]) for var in varnames]
        lat_j, lon_j = np.array([]), np.array([])
        for j in indj:
            vars_i = [np.array([]) for var in varnames]
            lat_i, lon_i = np.array([]), np.array([])
            for i in indi:
                filenamekji = filename+'_'+str(k)+'_'+str(j)+'_'+str(i)
                with xr.open_dataset(filenamekji+'.nc') as data:
                    for v in range(nvars):
                        vars_i[v] = np.append(vars_i[v],
                                              data[varnames[v]].values,
                                              axis=-1)
                    lat_i = np.append(lat_i, data[latname].values, axis=-1)
                    lon_i = np.append(lon_i, data[lonname].values, axis=-1)
                    if depname is not None:
                        dep_in = data[depname].values
                    if timname is not None:
                        tim_in = data[timname].values
            for v in range(nvars):
                vars_j[v] = np.append(vars_j, vars_i, axis=-2)
            lat_j = np.append(lat_j, lat_i, axis=-2)
            lon_j = np.append(lon_j, lon_i, axis=-2)
        for v in range(nvars):
            if NL[v] > 0:
                vars_k[v] = np.append(vars_k, vars_j, axis=-3)
            else:
                vars_k[v] = vars_j
        if depname is not None:
            dep_k = np.append(dep_k, dep_in)

    return vars_k, lat_j, lon_j, tim_in, dep_k
