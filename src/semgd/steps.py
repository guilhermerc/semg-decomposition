import numpy as np

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
