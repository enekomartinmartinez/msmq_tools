import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from msqg_tools.opends import load_1file


def partition_main(filename, denname, depname, latname, lonname,
                   savename, ind, nl, N, L0, timname=None,
                   method="max", plotname=None, nlsep=1, p=2,
                   depl=(0, 5000), inflay=False,
                   H=5000., L=50000., U=.1, g=9.81, den0=1029,
                   Ekb=0., Re=0., Re4=0., tau0=0.,
                   DT=5e-4, tend=2000., dtout=1., CLF=.5,
                   omega2=2*7.2921e-5, a=6.371e6):
    """
    Gives a discretization using the given method for the potential density.

    Parameters
    ----------
    method: ["grad", "max"]
        Name of the method to be used.
        max: Gives a discretization using the maximum mean potential
             density values difertence between layers.
             The maximum is given computing a p-norm,
             i.e., sum((den_i+1-den_i)**p).
        gra: Gives a discretization using the maximum gradient
             in potential density.
    nl: int
        Number of layers to be done.
    depl: (float, float)
        Estimated maximum depth for which the result is in the first layer.
        Estimated minimum depth for which the result is in the last layer.
        Makes the algorithm faster. Use dep = (0, H) to compute all values.
    nlsep: int
        The minimum number of layers to compute the subdivision. Default 1.
        Bigger value will make the algorithm faster.
        Minimum value must be 1.
    p: int (Only max method)
        The value of the p-norm to maximize.

    Returns
    -------
    ind: ndarray (1D)
        Array of the limits of each layer.
    """

    #############
    # LOAD DATA #
    #############

    [den], mlat, mlon, tim, dep = load_1file(filename, [denname],
                                             latname, lonname,
                                             depname, timname)

    ind = dep < H
    den, dep = den[:, ind], dep[ind]

    mden = np.mean(den, axis=0)

    # Defining minimum and maximum index to compute between
    if depl[0] <= dep[0]:
        imin = 1
    else:
        imin = np.min(np.where(dep >= depl[0]))

    if depl[1] >= H:
        imax = len(dep)
    else:
        imax = np.max(np.where(dep <= depl[1]))

    # Starts the method
    if method == "grad":
        ind = make_partition_grad(mden, dep, nl, nlsep, (imin, imax))
    elif method == "max":
        ind = make_partition_max(mden, nl, nlsep,  (imin, imax), p)

    # Adding first and last index to ind
    ind = np.insert(ind, (0, nl-1), [0, len(dep)]).astype(int)

    # Plotting
    if plotname is not None:
        plot_dis(plotname, mden, dep, ind, H)

    ###################
    # SAVE PARAMETERS #
    ###################

    create_params_file(savename, dep, mden, ind, mlat, nl, N, L0,
                       Ekb, Re, Re4, tau0, DT, tend, dtout, CLF,
                       inflay, H, L, U, g, den0, omega2, a)

    ###################################
    # RETURN DISCRETIZATION DENSITIES #
    ###################################

    return (dep[ind[1:-1]], mden[ind[1:-1]])


def make_partition_grad(mden, dep, nl, nlsep, ilim):

    # Computes the density gradient
    dpden = np.diff(mden[ilim[0]:ilim[1]])\
            / np.diff(dep[ilim[0]:ilim[1]])
    m = len(dpden)
    # initialize index and maximum number of loops
    ind = []
    while len(ind) < (nl-1):
        # find the index of the maximum gradient value
        tind = np.argmax(dpden)
        ind.append(tind)
        # set used value and neightbours to 0
        dpden[max(tind-nlsep, 0):min(tind+nlsep, m)] = 0
        if np.all(dpden <= 0):
            raise ValueError('No convergence')
    # add minimum index and sort them
    ind = ilim[0] + np.sort(ind)
    return ind


def make_partition_max(mden, nl, nlsep, ilim, p):

    # Generate combinations of partitions
    comb = combinations(np.arange(ilim[0], ilim[1]), nl-1)
    maxval = 0
    for c in comb:
        if np.any(np.diff(c) <= nlsep):
            # if in a combination layers are close go to the next one
            continue
        # split and compute the mean values norm
        sh = np.split(deltah, c)
        sp = np.split(den, c)
        msp = np.array([np.average(p, weights=h) for p, h in zip(sp, sh)])
        norm = np.sum(np.diff(msp)**p)
        if norm > maxval:
            # if norm is bigger than current value save new combination
            maxval = norm
            ind = c
    return ind


def create_params_file(savename, dep, den, ind, mlat, nl, N, L0,
                       Ekb, Re, Re4, tau0, DT, tend, dtout, CLF,
                       inflay, H, L, U, g, den0, omega2, a):

    params = get_params(dep, den, ind, mlat, inflay,
                        H, L, U, g, den0, omega2, a)

    with open(savename, "w") as f:
        f.write("#!sh\n"
                + "# " + savename + "\n"
                + "# input parameter files\n"
                + "# Generated with python\n\n"
                + "# domain size\n"
                + "N  = {}\n".format(N)
                + "nl = {}\n".format(nl)
                + "L0 = {}\n\n".format(L0/L)
                + "# physical parameters\n"
                + "Rom   = -{}\n".format(params[2])
                + "Ekb   = {}\n".format(Ekb)
                + "Re    = {}\n".format(Re)
                + "Re4   = {}\n".format(Re4)
                + "beta  = {}\n".format(params[3])
                + "tau0  = {}\n".format(tau0)
                + "Fr = ["
                + ",".join([str(params[1][i]) for i in range(nl-1)])
                + "]\ndh = ["
                + ",".join([str(params[0][i]) for i in range(nl)])
                + "]\nbreak_den = ["
                + ",".join([str(den[i]) for i in ind[1:-1]])
                + "]\n\n"
                + "# timestepping\n"
                + "DT = {}\n".format(DT)
                + "tend  = {}\n".format(tend)
                + "dtout = {}\n".format(dtout)
                + "CFL   = {}".format(CLF))


def get_params(dep, den, ind, mlat, inflay,
               H, L, U, g, den0, omega2, a):

    deltah = np.gradient(dep)
    sh = np.split(deltah, ind[1:-1])
    sp = np.split(den, ind[1:-1])
    msp = np.array([np.average(p, weights=h) for p, h in zip(sp, sh)])
    dp = np.diff(msp)
    if inflay:
        H *= 10
        dep[-1] = H
    ind[-1] = ind[-1] - 1
    dh = (dep[ind[1:]] - dep[ind[:-1]])
    h2 = .5 * (dh[1:]+dh[:-1])
    dh = dh/H
    N = np.sqrt(g*dp/(h2*den0))
    Fr = U/(N*H)
    f = omega2*np.sin(np.deg2rad(mlat))
    Ro = U/(f*L)
    beta = omega2/a*np.cos(np.deg2rad(mlat))*L**2/U
    return (dh, Fr, Ro, beta)


def plot_dis(plotname, den, dep, ind, H):

    plt.plot(den, dep, label="mean profile")
    label2 = "discretization"
    for i in range(len(ind)-1):
        mdeni = np.mean(den[ind[i]:ind[i+1]])
        plt.vlines(mdeni, dep[ind[i]], dep[ind[i+1]-1],
                   label=label2, ls=':')
        label2 = None
    plt.ylabel(r"Depth ($m$)")
    plt.xlabel(r"Potetial density ($kg\,m^{-3}$)")
    plt.ylim(H, 0)
    plt.savefig(plotname)
    plt.close()
    print(plotname+' saved')
