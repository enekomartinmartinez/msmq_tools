import dask
import numpy as np
import xarray as xr
from scipy.interpolate import griddata


def int_main(filename, savename, varnames,
             latname, lonname, mlat, mlon,
             L0, N0=512, Nlim=0, NL=None,
             depname=None, timname=None,
             tb=None, zb=None,
             yb=None, xb=None,
             Lind=None, method='cubic', parallel=False):

    N = N0 - Nlim
    L = L0 / N0 * N

    #############
    # LOAD DATA #
    #############
    print("Loading data")

    vars_in = []

    ##############
    # CREATE DIM #
    ##############
    print("Creating dimensions")

    x = np.linspace(-L/2, L/2, N)
    X, Y = np.meshgrid(x, x)
    lat_out = mlat + Y/111000
    lon_out = mlon + X/111000/np.cos(np.deg2rad(lat_out))

    NT = vars_in[0].shape[0]

    vars_out = []
    if NL > 0:
        for i in range(len(varnames)):
            if NL[i] > 0:
                vars_out.append(np.empty((NT, NL, N, N)))
            else:
                vars_out.append(np.empty((NT, N, N)))

    lat_inr = lat_in.ravel()
    lon_inr = lon_in.ravel()
    lat_outr = lat_out.ravel()
    lon_outr = lon_out.ravel()

    #################
    # INTERPOLATION #
    #################

    for v in range(len(varnames)):
        print("Interpolating " + varnames[v])
        int_var(vars_in[v], lat_inr, lon_inr,
                NT, NL, lat_outr, lon_outr,
                N, method, parallel)
    #############
    # SAVE DATA #
    #############

    if split:
        savename = savename[:-3]
        Nb = int(N/Nbox)
        for i in range(4):
            for j in range(4):
                savenameij = savename+'_'+str(i)+'_'+str(j)+'.nc'
                ds = {lonname: (('y', 'x'), lon_out[i*Nb:(i+1)*Nb,
                                                    j*Nb:(j+1)*Nb]),
                      latname: (('y', 'x'), lat_out[i*Nb:(i+1)*Nb,
                                                    j*Nb:(j+1)*Nb])}

                if depname is not None and depname is not '':
                    ds[depname] = (('z'), dep_in)

                if timname is not None and timname is not '':
                    ds[timname] = (('t'), tim_in)

                for l in range(nvars):
                    if NL[l] > 0:
                        ds[varnames[l]] = (('time', 'z', 'y', 'x'),
                                            vars_out[l][:, :,
                                                        i*Nb:(i+1)*Nb,
                                                        j*Nb:(j+1)*Nb])
                    else:
                        ds[varnames[l]] = (('time', 'y', 'x'),
                                            vars_out[l][:,
                                                        i*Nb:(i+1)*Nb,
                                                        j*Nb:(j+1)*Nb])

                ds = xr.Dataset(ds)
                ds.to_netcdf(savenameij)

    else:
        ds = {lonname: (('y', 'x'), lon_out),
              latname: (('y', 'x'), lat_out)}

        if depname is not None and depname is not '':
            ds[depname] = (('z'), dep_in)

        if timname is not None and timname is not '':
            ds[timname] = (('t'), tim_in)

        for i in range(nvars):
            if NL[i] > 0:
                ds[varnames[i]] = (('time', 'z', 'y', 'x'), vars_out[i])
                vars_out[i] = None
            else:
                ds[varnames[i]] = (('time', 'y', 'x'), vars_out[i])
                vars_out[i] = None

        ds = xr.Dataset(ds)
        ds.to_netcdf(savename)


def int_var(var_in, lat_inr, lon_inr,
            NT, NL, lat_outr, lon_outr,
            N, method, parallel):

    if NL > 0:
        var_out = np.empty_like((NT, NL, N, N))
    else:
        var_out = np.empty_like((NT, N, N))

    if parallel and NT > 1:
        if NL > 0:
            for l in range(NL):
                print(str(round((l)/NL*100, 2))+'%')

                def inter(t):
                    print('Computing time ' + str(t))
                    var_out[t, l] = griddata((lon_inr, lat_inr),
                                             var_in[t, l].ravel(),
                                             (lon_outr, lat_outr),
                                             method=method).reshape((N, N))
                    return 1
                output = []
                for i in range(NT):
                    run_paral = dask.delayed(inter)(i)
                    output.append(run_paral)
                total = dask.delayed(sum)(output)
                total.compute()
        else:
            def inter(t):
                print('Computing time '+str(t))
                var_out[t] = griddata((lon_inr, lat_inr),
                                      var_in[t].ravel(),
                                      (lon_outr, lat_outr),
                                      method=method).reshape((N, N))
                return 1
            output = []
            for i in range(NT):
                run_paral = dask.delayed(inter)(i)
                output.append(run_paral)
            total = dask.delayed(sum)(output)
            total.compute()

    else:
        if NL > 0:
            for l in range(NL):
                for t in range(NT):
                    print(str(round((l+1)/NL*t/NT*100, 2))+'%')
                    var_out[t, l] = griddata((lon_inr, lat_inr),
                                             var_in[t, l].ravel(),
                                             (lon_outr, lat_outr),
                                             method=method).reshape((N, N))
        else:
            for t in range(NT):
                print(str(round(t/NT*100, 2))+'%')
                var_out[t] = griddata((lon_inr, lat_inr),
                                      var_in[t].ravel(),
                                      (lon_outr, lat_outr),
                                      method=method).reshape((N, N))

    return var_out
