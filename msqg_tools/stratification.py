import dask
import numpy as np
import xarray as xr
from scipy.interpolate import interp1d
from msqg_tools.opends import load_main
from msqg_tools.tools import int2iterable, split_iterable


def stra_main(file_den, file_str, bpnt, denname, latname, lonname,
              depname, strname, timname=None, Nproc=1, ind=None, H=5000):

    if ind is None:
        stra_1file(file_den, file_str, bpnt, denname, latname, lonname,
                   depname, strname, timname, H)

    else:
        def str_kji(kji):
            k, j, i = kji
            fden = file_den + '_' + str(k) + '_' + str(j) + '_' + str(i)
            fstr = file_str + '_' + str(k) + '_' + str(j) + '_' + str(i)
            stra_1file(fden, fstr, bpnt, denname, latname, lonname,
                       depname, strname, timname, H)
            return 1

        # Get iterables for the 3 index and call combinations
        indk = int2iterable(ind[0])
        indj = int2iterable(ind[1])
        indi = int2iterable(ind[2])

        for k in indk:
            kji_com = [(k, j, i) for j in indj for i in indi]
            totl = len(kji_com)

            # Run in parallel
            if Nproc > 1:
                kji_com = split_iterable(kji_com, Nproc)
                print("Processing {} files with {} cores".format(totl,
                                                                 Nproc))
                totl = len(kji_com)
                for i, kji_ in enumerate(kji_com):
                    print("\t{:.2f}%".format(100.*i*(k+1)/totl))
                    output = []
                    for kji in kji_:
                        run_paral = dask.delayed(str_kji)(kji)
                        output.append(run_paral)
                    total = dask.delayed(sum)(output)
                    total.compute()

            # Run in series
            else:
                print("Processing {} files".format(totl))
                for i, kji_ in enumerate(kji_com):
                    print("\t{:.2f}%".format(100.*i*(k+1)/totl))
                    str_kji(kji_)

        [strval], lats, lons, tim, _ = load_main(file_str, [strname],
                                                 latname, lonname,
                                                 None, timname, ind)

        ds = {lonname: (('y', 'x'), lons),
              latname: (('y', 'x'), lats),
              strname: (('t', 'z', 'y', 'x'), strval)}

        if timname is not None:
            ds[timname] = (('t'), tim)

        ds = xr.Dataset(ds)
        ds.to_netcdf(file_str+'.nc')


def stra_1file(file_den, file_str, bpnt, denname, latname, lonname,
               depname, strname, timname, H):

    #############
    # LOAD DATA #
    #############

    [den], lats, lons, tim, dep = load_main(file_den, [denname],
                                            latname, lonname,
                                            depname, timname)
    #dind = np.logical_and(dep > 500, dep < 2000)
    #den, dep = den[:, dind], dep[dind]

    dim = den.shape

    strval = np.empty((dim[0], len(bpnt[0]), dim[2], dim[3]))

    for k, (h, p) in enumerate(zip(bpnt[0], bpnt[1])):
        dind = np.logical_and(dep > h-250, dep < h+250)
        denk, depk = den[:, dind], dep[dind]
        
        for t in range(dim[0]):
            for j in range(dim[2]):
                for i in range(dim[3]):
                    nonanval = ~np.isnan(denk[t, :, j, i])
                    denkji = denk[t, nonanval, j, i]
                    depkji = depk[nonanval]
                    if len(depkji) == 0\
                       or p < np.min(denkji)\
                       or p > np.max(denkji):
                         strval[t, k, j, i] = np.nan
                         print("nan value encountered")
                    else:
                        strval[t, k, j, i] =\
                            interp1d(denkji, depkji, kind='cubic')(p)

    ds = {lonname: (('y', 'x'), lons),
          latname: (('y', 'x'), lats),
          strname: (('t', 'z', 'y', 'x'), strval)}

    if timname is not None:
        ds[timname] = (('t'), tim)

    ds = xr.Dataset(ds)
    ds.to_netcdf(file_str+'.nc')
