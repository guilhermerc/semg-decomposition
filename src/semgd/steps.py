import numpy as np
from scipy.signal import find_peaks
from scipy.stats import variation
from sklearn.cluster import KMeans

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

def refinement(z, w_i, TH_SIL, max_iter):
    "Steps 4, 5 and 6"
    # 4. Initialize CoV_{n - 1} and CoV_n
    cov_curr = np.random.rand(1)

    n = 0
    # 5. While CoV_n < CoV_{n - 1}
    while True:

        # a. Estimate the i-th source
        s = np.dot(w_i.T, z)

        # b. Estimate the pulse train PT_n with peak detection and K-means class
        s = np.square(s)

        peaks_idxs, _ = find_peaks(s, distance=20)  # 20 samples @ 2048 Hz is
                                            	    # equiv. to approx. 10 ms

        PT = np.zeros_like(s)
        for idx in peaks_idxs:
            PT[idx] = 1

        kmeans = KMeans(n_clusters=2).fit(s[peaks_idxs].T.reshape(-1, 1))
        centroids = kmeans.cluster_centers_

        peaks_clus = kmeans.predict(s[peaks_idxs].T.reshape(-1, 1))

        t_j = []
        for peak in range(len(peaks_idxs)):
        	if peaks_clus[peak] == 0:
        		t_j.append([peaks_idxs[peak]])
        t_j = np.array(t_j)
        J = len(t_j)

        PT_n = np.zeros(len(s))
        for t in t_j:
        	PT_n[t] = 1

        # c. Set CoV_{n - 1} = CoV_n and calculate CoV_n of PT_n
        cov_last = cov_curr

        ISI = np.zeros(len(t_j) - 1) #
        for k in range(1, len(t_j)):
            ISI[k - 1] = t_j[k] - t_j[k - 1]

        cov_curr = variation(ISI)

        # d. w_i(n + 1) = (1/J) \sum_{J = 1}^{J} z(t_j)
        w_i = np.zeros_like(w_i)
        for t in t_j:
            # TODO: Something really weird is happening here
            w_i = w_i + ((1/J)*z[:, t])
        w_i = w_i[:, 1]

        # e. Set n = n + 1
        n = n + 1

        if cov_curr > cov_last or n > max_iter:
            break

    # End while CoV(n) < CoV(n - 1)

    s_clus = kmeans.predict(s.T.reshape(-1, 1))

    within_sum, betw_sum = 0, 0
    for k in range(len(s)):
        within_sum = within_sum + np.linalg.norm(s[k] - centroids[s_clus[k], 0])
        betw_sum = betw_sum + np.linalg.norm(s[k] - centroids[1 - s_clus[k], 0])

    SIL = abs(within_sum - betw_sum)/max(within_sum, betw_sum)

    # 6. If SIL > 0.9
    # a. Accept the source estimate
    # b. Add w_i to the matrix B
    if SIL < TH_SIL:
        w_i = np.zeros_like(w_i)

    return w_i
