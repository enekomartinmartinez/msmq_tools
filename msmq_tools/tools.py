import numpy as np

def create_partition(Npar, Ndots):
    """
    Creates a array with the indexis to split the data.

    Parameters
    ----------
    Npar : int
        Number of partitions to be done.
    Ndots : int
        Total number of index to be splitted.

    Returns
    -------
    Ndpp : ndarray
        1 dimensional array with the values where the data must be splitted.

    """
    Ndpp = np.arange(Npar+1)
    if (Ndots % Npar) == 0:
        Ndpp *= int(Ndots/Npar)
    else:
        Ndpp *= int(Ndots/Npar)+1
        Ndpp[-1] = Ndots
    return Ndpp


def int2iterable(val):
    """
    Returns iterable object

    Parameters
    ----------
    val : int or array like

    Returns
    -------
    Iterable
        If a given variable is a int, returns a list with the original value.
        Else returns the original value.

    """
    if type(val) is int:
        return [val]
    else:
        return val

def split_iterable(ite, x):
    """
    Splits a iterable in a given length sublist.

    Parameters
    ----------
    ite : array like
        iterable to be splitted.
    x : int
        length of the sublists.

    Returns
    -------
    List
        Splitted list.

    """
    return [ite[i:i+x] for i in range(0, len(ite), x)]
