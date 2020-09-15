import numpy as np

def subtract_mean(x):
    "1. Subtract the mean from the observations x"
    for channel in x:
        channel[...] = channel - np.mean(channel)
