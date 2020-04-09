import dask
import numpy as np
import xarray as xr
from msqg_tools.opends import load_1file
from msqg_tools.tools import int2iterable, split_iterable


def stra_main(filename, maskname, varname, latname, lonname,
                 depname=None, timname=None, gridval=None,
                 Nproc=1, ind=None):

    if ind is None:
        stra_1file(filename,

    else:
        def str_kji(kji):
            k, j, i = kji
            fname = filename + '_' + str(k) + '_' + str(j) + '_' + str(i)
            stra_1file(fname,
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


def stra_1file(filename,

    #############
    # LOAD DATA #
    #############

    [den], lats, lons, tim, dep = load_1file(filename, [denname],
                                             latname, lonname,
                                             depname, timname)


