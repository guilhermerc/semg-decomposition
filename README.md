# semg-decomposition

#### Progress tracking

The following algorithm is described on Negro et al. (J. Neural Engineering,
2015) - page 3:

- [x] Extend the observations x by a R factor
- [x] Subtract the mean from the observations x
- [x] Whiten x
- [x] Initialize the matrix B to empty matrix
- [x] For i = 1, 2, ..., M repeat:
    - [x] 1. Initialize the vector w\_i(0) and w\_i(-1)
    
    - [x] 2. While |w\_i(n)^{T}w\_i(n - 1) - 1| < Tolx<br>
          &nbsp;&nbsp;&nbsp;&nbsp;a. Fixed point algorithm<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;w_i(n) = E{zg[w_i(n - 1)^{T}z]} - Aw_i(n - 1)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;with A = E{g'[w_i(n - 1)^{T}z]}<br>
          &nbsp;&nbsp;&nbsp;&nbsp;b. Orthogonalization<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;w_i(n) = w_i(n) - BB^{T}w_i(n)<br>
          &nbsp;&nbsp;&nbsp;&nbsp;c. Normalization<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;w_i(n) = w_i(n)/||w_i(n)||<br>
          &nbsp;&nbsp;&nbsp;&nbsp;d. Set n = n + 1<br>
    - [x] 3. End while
    
    - [x] 4. Initialize CoV_{n - 1} and CoV\_n
    
    - [x] 5. While CoV\_n < CoV_{n - 1}<br>
          &nbsp;&nbsp;&nbsp;&nbsp;a. Estimate the i-th source<br>
          &nbsp;&nbsp;&nbsp;&nbsp;b. Estimate the pulse train PT_n with peak detection and K-means class<br>
          &nbsp;&nbsp;&nbsp;&nbsp;c. Set CoV_{n - 1} = CoV_n and calculate CoV_n of PT_n<br>
          &nbsp;&nbsp;&nbsp;&nbsp;d. w_i(n + 1) = (1/J) \sum_{J = 1}^{J} z(t_j)<br>
          &nbsp;&nbsp;&nbsp;&nbsp;e. Set n = n + 1<br>
          
      End while CoV(n) < CoV(n - 1)
      
    - [x] 6. If SIL > 0.9<br>
          &nbsp;&nbsp;&nbsp;&nbsp;a. Accept the source estimate<br>
          &nbsp;&nbsp;&nbsp;&nbsp;b. Add w_i to the matrix B<br>
          
    End for loop
