import numpy as np

from .spars_meas_func import g, g_der

def extend(x, R):
    "Extend the observations x by a R factor"
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
    "Subtract the mean from the observations x"
    for channel in x:
        channel[...] = channel - np.mean(channel)

def whiten(x):
    "Whiten x"
    d, U = np.linalg.eigh(np.cov(x))
    D = np.diag(d)

    # Regularization
    reg_fact = d[:round(len(d)/2)].mean()

    for i in range(round(len(d)/2)):
        d[i] = reg_fact

    # W = UD^{-1/2}U.T
    W = np.dot(U, np.dot(np.sqrt(np.linalg.inv(D)), U.T))

    return np.dot(W, x)

def separation(z, B, Tolx, max_iter):
    "Steps 1, 2 and 3"
    # 1. Initialize the vector w_i(0) and w_i(-1)
    m, D_r = z.shape
    w_new = np.random.rand(m)

    # 2. While |w_i(n)^{T}w_i(n - 1) - 1| < Tolx
    n = 0
    while True:
        w_old = w_new

        # a. Fixed point algorithm
        # w_i(n) = E{zg[w_i(n - 1)^{T}z]} - Aw_i(n - 1)
        # with A = E{g'[w_i(n - 1)^{T}z}
        A = g_der(np.dot(w_old.T, z)).mean()
        w_new = (z*g(np.dot(w_old.T, z))).mean(axis=1) - A*w_old

        # b. Orthogonalization
        # w_i(n) = w_i(n) - BB^{T}w_i(n)
        w_new = w_new - np.dot(np.dot(B.T, w_new), B)

        # c. Normalization
        # w_i(n) = w_i(n)/||w_i(n)||
        if np.linalg.norm(w_new) > 0:
            w_new = w_new/np.linalg.norm(w_new)

        # d. Set n = n + 1
        n = n + 1

        if np.linalg.norm(np.dot(w_new.T, w_old) - 1) < Tolx or n > max_iter:
            break

    # 3. End while
    return w_new
