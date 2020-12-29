import numpy as np

def extend(x, R):
    "0. Extend the observations x by a R factor"
    m, D_r = x.shape

    # Builts the extended observations matrix ('x_') by slicing an auxiliary
    # matrix ('x'), which is the original observations matrix appended with 'R'
    # columns of 0s at the beginning.
    x = np.hstack((np.zeros((m, R)), x))

    x_ = np.empty((m*(R + 1), D_r))
    for ch in range(m):
        for r in range(R + 1):
            x_[ch*(R + 1) + r] = x[ch, R - r:R - r + D_r]

    return x_

def subtract_mean(x):
    "1. Subtract the mean from the observations x"
    for channel in x:
        channel[...] = channel - np.mean(channel)

def whiten(x):
    "2. Whiten x"
    d, U = np.linalg.eigh(np.cov(x))
    D = np.diag(d)

    # Regularization
    reg_fact = d[:round(len(d)/2)].mean()

    for i in range(round(len(d)/2)):
        d[i] = reg_fact

    # W = UD^{-1/2}U.T
    W = np.dot(U, np.dot(np.sqrt(np.linalg.inv(D)), U.T))

    return np.dot(W, x)
