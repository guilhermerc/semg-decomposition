import numpy as np

# Sparseness measurement function used on step 2.a. Fixed point algorithm

def g(x):
    return np.log(np.cosh(x))

def g_der(x):
    return np.tanh(x)
