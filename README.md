# semg-decomposition

#### Progress tracking

The following algorithm is described on Negro et al. (J. Neural Engineering,
2015) - page 3:

- [x] Extend the observations x by a R factor
- [x] Subtract the mean from the observations x
- [x] Whiten x
- [ ] Initialize the matrix B to empty matrix
- [ ] For i = 1, 2, ..., M repeat:
    - [x] 1. Initialize the vector w\_i(0) and w\_i(-1)
    - [x] 2. While |w\_i(n)^{T}w\_i(n - 1) - 1| < Tolx
          a. Fixed point algorithm
          w_i(n) = E{zg[w_i(n - 1)^{T}z]} - Aw_i(n - 1)
          with A = E{g'[w_i(n - 1)^{T}z}
          b. Orthogonalization
          w_i(n) = w_i(n) - BB^{T}w_i(n)
          c. Normalization
          w_i(n) = w_i(n)/||w_i(n)||
          d. Set n = n + 1
    - [x] 3. End while
    - (...)
