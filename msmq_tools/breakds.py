import numpy as np
import xarray as xr
from opends import load_1file


def breakds(filename, varnames, latname, lonname,
            NL, Nbx=1, Nby=1, Nbz=1,
            depname=None, timname=None,
            tb=(None, None), zb=(None, None),
            yb=(None, None), xb=(None, None)):

    #############
    # LOAD DATA #
    #############

    print("Loading data")

    vars_in, lat, lon, tim, dep = load_1file(filename, varnames,
                                             latname, lonname,
                                             depname, timname, NL,
                                             tb=tb, zb=zb, yb=yb, xb=xb)

    def create_partition(Npar, Ndots):
        Ndpp = np.arange(Npar+1)
        if (Ndots % Npar) == 0:
            Ndpp *= int(Ndots/Npar)
        else:
            Ndpp *= int(Ndots/Npar)+1
            Ndpp[-1] = Ndots
        return Ndpp

    svar = vars_in.shape
    # NT = svar[0]
    Nk = create_partition(Nbz, svar[1])
    Nj = create_partition(Nby, svar[2])
    Ni = create_partition(Nbx, svar[3])

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
                    if NL[v] > 0:
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
