import numpy as np

def extend(x, R):
    "0. Extend the observations x by a R factor"
    m, D_r = x.shape

    # Builts the extended observations matrix ('x_tilde') by reverse slicing an
    # auxiliary matrix ('x_aux'), which is the observations matrix ('x')
    # appended with 'R' columns of 0s at the beginning.
    x_aux = np.hstack((np.zeros((m, R)), x))
    for j in range(D_r):
        if j == 0:
            x_tilde = np.array((x_aux.T[R::-1]).T)
        else:
            x_tilde = np.hstack((x_tilde, (x_aux.T[R + j:j - 1:-1]).T))

    return x_tilde


def subtract_mean(x):
    "1. Subtract the mean from the observations x"
    for channel in x:
        channel[...] = channel - np.mean(channel)

def whiten(x):
    "2. Whiten x"
    d, U = np.linalg.eigh(np.cov(x))
    D = np.diag(d)

    # W = UD^{-1/2}U.T
    W = np.dot(U, np.dot(np.sqrt(np.linalg.inv(D)), U.T))

    return np.dot(W, x)
