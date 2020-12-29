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
    - [x] 4. Initialize CoV_{n - 1} and CoV\_n
    - [x] 5. While CoV\_n < CoV_{n - 1}
          a. Estimate the i-th source
          b. Estimate the pulse train PT_n with peak detection and K-means class
          c. Set CoV_{n - 1} = CoV_n and calculate CoV_n of PT_n
          d. w_i(n + 1) = (1/J) \sum_{J = 1}^{J} z(t_j)
          e. Set n = n + 1
      End while CoV(n) < CoV(n - 1)
    - [x] 6. If SIL > 0.9
          a. Accept the source estimate
          b. Add w_i to the matrix B
