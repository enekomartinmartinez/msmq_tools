import dask
import numpy as np
import xarray as xr
from scipy.interpolate import griddata
from msqg_tools.opends import load_main
from msqg_tools.tools import split_iterable


def int_main(filenames, varnames,
             latname, lonname, mlat, mlon,
             L0, N0=512, Nlim=0,
             depname=None, timname=None,
             method='cubic', Nproc=1, parallel='time', ind=None):

    N = N0 - 2*Nlim
    DX = L0 / N0
    L = DX * N
    L2 = (L-DX)/2

    ##############
    # CREATE DIM #
    ##############

    x = np.linspace(-L2, L2, N)
    X, Y = np.meshgrid(x, x)
    lat_out = mlat + Y/111000
    lon_out = mlon + X/111000/np.cos(np.deg2rad(lat_out))

    lat_outr = lat_out.ravel()
    lon_outr = lon_out.ravel()

    if type(filenames) is str:
        int_1file(filenames, varnames, latname,
                  lonname, depname, timname,
                  lat_out, lat_outr, lon_out, lon_outr,
                  N, method, Nproc, parallel, ind)

    else:
        def int_f(filename):
            int_1file(filename, varnames, latname,
                      lonname, depname, timname,
                      lat_out, lat_outr, lon_out, lon_outr,
                      N, method, Nproc, parallel, ind)
            return 1

        totl = len(filenames)
        if (Nproc > 1) and (len(filenames) > 1) and (parallel == 'file'):
            filenames = split_iterable(filenames, Nproc)
            print("Processing {} files with {} cores".format(totl, Nproc))
            totl = len(filenames)
            for i, filenames_ in enumerate(filenames):
                print("\t{:.2f}%".format(100.*i/totl))
                output = []
                for filen in filenames_:
                    run_paral = dask.delayed(int_f)(filen)
                    output.append(run_paral)
                total = dask.delayed(sum)(output)
                total.compute()

        else:
            print("Processing {} files".format(totl))
            for i, filen in enumerate(filenames):
                print("\t{:.2f}%".format(100.*i/totl))
                int_f(filen)


def int_1file(filename, varnames, latname, lonname, depname, timname,
              lat_out, lat_outr, lon_out, lon_outr,
              N, method, Nproc, parallel, ind):

    #############
    # LOAD DATA #
    #############
    print("Loading data from " + filename + ".nc")

    vars_in, lat_in, lon_in, tim, deps = load_main(filename, varnames,
                                                   latname, lonname,
                                                   depname, timname,
                                                   ind)

    NT = vars_in[0].shape[0]
    NL = []
    for var in vars_in:
        if len(var.shape) == 4:
            NL.append(var.shape[1])
        else:
            NL.append(0)

    vars_out = []
    for nl in NL:
        if nl > 0:
            vars_out.append(np.empty((NT, nl, N, N)))
        else:
            vars_out.append(np.empty((NT, N, N)))

    lat_inr = lat_in.ravel()
    lon_inr = lon_in.ravel()

    #################
    # INTERPOLATION #
    #################

    def int_v(v):
        print("\tInterpolating " + varnames[v])
        vars_out[v] = int_var(vars_in[v], lat_inr, lon_inr,
                              NT, NL[v], lat_outr, lon_outr,
                              N, method, Nproc, parallel)
        return 1

    if (Nproc > 1) and (len(vars_out) > 1) and (parallel == 'var'):
        output = []
        for v in range(len(varnames)):
            run_paral = dask.delayed(int_v)(v)
            output.append(run_paral)
        total = dask.delayed(sum)(output)
        total.compute()
    else:
        for v in range(len(varnames)):
            int_v(v)

    #############
    # SAVE DATA #
    #############

    ds = {lonname: (('y', 'x'), lon_out),
          latname: (('y', 'x'), lat_out)}

    if depname is not None:
        ds[depname] = (('z'), deps)

    if timname is not None:
        ds[timname] = (('t'), tim)

    for nl, var, varn in zip(NL, vars_out, varnames):
        if nl > 0:
            ds[varn] = (('t', 'z', 'y', 'x'), var)
        else:
            ds[varn] = (('t', 'y', 'x'), var)

    ds = xr.Dataset(ds)
    ds.to_netcdf(filename + '_' + str(N) + 'x' + str(N) + '.nc')


def int_var(var_in, lat_inr, lon_inr,
            NT, NL, lat_outr, lon_outr,
            N, method, Nproc, parallel):

    if NL > 0:
        var_out = np.empty((NT, NL, N, N))
        for z in range(NL):
            var_in[:, z][np.isnan(var_in[:, z])] = np.nanmean(var_in[:, z])
    else:
        var_out = np.empty((NT, N, N))
        var_in[np.isnan(var_in)] = np.nanmean(var_in)

    if (Nproc > 1) and (NT > 1) and (parallel == 'time'):
        times = split_iterable(np.arange(NT), Nproc)
        print("\tProcessing {} times with {} cores".format(NT, Nproc))
        if NL > 0:
            for l in range(NL):
                print("\t\t{:.2f}%".format(100.*l/NL))

                def inter(t):
                    var_out[t, l] = griddata((lon_inr, lat_inr),
                                             var_in[t, l].ravel(),
                                             (lon_outr, lat_outr),
                                             method=method).reshape((N, N))
                    return 1

                for times_ in times:
                    output = []
                    for time in times_:
                        run_paral = dask.delayed(inter)(time)
                        output.append(run_paral)
                    total = dask.delayed(sum)(output)
                    total.compute()
        else:
            def inter(t):
                var_out[t] = griddata((lon_inr, lat_inr),
                                      var_in[t].ravel(),
                                      (lon_outr, lat_outr),
                                      method=method).reshape((N, N))
                return 1

            totl = len(times)
            for i, times_ in enumerate(times):
                print("\t\t{:.2f}%".format(100.*i/totl))
                output = []
                for time in times_:
                    run_paral = dask.delayed(inter)(time)
                    output.append(run_paral)
                total = dask.delayed(sum)(output)
                total.compute()

    else:
        if NL > 0:
            for l in range(NL):
                for t in range(NT):
                    print('\t\t{:.2f}%'.format((l+1)/NL*t/NT*100))
                    var_out[t, l] = griddata((lon_inr, lat_inr),
                                             var_in[t, l].ravel(),
                                             (lon_outr, lat_outr),
                                             method=method).reshape((N, N))
        else:
            for t in range(NT):
                print('\t\t{:.2f}%'.format(t/NT*100))
                var_out[t] = griddata((lon_inr, lat_inr),
                                      var_in[t].ravel(),
                                      (lon_outr, lat_outr),
                                      method=method).reshape((N, N))

    return var_out
