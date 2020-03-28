import sys
import dask
import numpy as np
import xarray as xr
from scipy.interpolate import griddata


def int_main(filename, varname, timname, latname, lonname, 
             L0, N0=512, Nlim=0, NL=None,
             tb=(None, None), zb=(None, None),
             yb=(None, None), xb=(None, None),
             depname=None, Lind=None, parallel=False):

    N = N0 - Nlim
    L = L0 / N0 * N


    #############
    # LOAD DATA #
    #############
    print("Loading data")
   
    vars_in = []

    with xr.open_dataset(path2data+filename) as data:
        for i in range(len(varnames)):
            if NL[i] > 0:
                vars_in.append(data[varnames[i]].values[tb[0]:tb[1], 
                                                        zb[0]:zb[1],
                                                        yb[0]:yb[1], 
                                                        xb[0]:xb[1]])
            else:
                vars_in.append(data[varname].values[tb[0]:tb[1],
                                                    yb[0]:yb[1], 
                                                    xb[0]:xb[1]])
        lat_in = data[latname].values[yb[0]:yb[1], 
                                      xb[0]:xb[1]]
        lon_in = data[lonname].values[yb[0]:yb[1], 
                                      xb[0]:xb[1]]
        if depname is not None and depname is not '':
            dep_in = data[depname].values[zb[0]:zb[1]]
        if timname is not None and timname is not '':
            tim_in = data[timname].values[tb[0]:tb[1]]
    
    ##############
    # CREATE DIM #
    ##############
    print("Creating dimensions")
    
    x = np.linspace(-L/2, L/2, N)
    X, Y = np.meshgrid(x,x)
    lat_out = mlat + Y/111000
    lon_out = mlon + X/111000/np.cos(np.deg2rad(lat_out))
    
    NT = var_in.shape[0]

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

    # LAUNCH INTERPOLATION

    #############
    # SAVE DATA #
    #############
    
    if split:
        savename = savename[:-3
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
                ds.to_netcdf(path2save + savenameij)

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
        ds.to_netcdf(path2save + savename)


def int_var(var_in, lat_inr, lon_inr, 
            NT, NL, lat_outr, lon_outr,
            varname, parallel=False):
    
    #################
    # INTERPOLATION #
    #################
    print("Interpolating " + varname)

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
                                            (lon_outr,lat_outr),
                                            method=method).reshape((N, N))
        else:
            for t in range(NT):
                print(str(round(t/NT*100, 2))+'%')
                var_out[t] = griddata((lon_inr, lat_inr),
                                      var_in[t].ravel(),
                                      (lon_outr, lat_outr),
                                      method=method).reshape((N, N))

    return var_out    
