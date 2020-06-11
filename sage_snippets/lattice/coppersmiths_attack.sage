def construct_polynomial_matrix(n, N, a, X):                                                           
    M = [[N] + [0]*(n-1)]
    for i in range(n-1):
        M.append([0]*i + [a*X**i, X**(i+1)] + [0]*(n-2-i))
    return M

def coppersmith(a, bits, N, n):                                                                        
    X = 2^(1024-bits)
    a2 = int(gmpy2.invert(2**bits,N))
    M = matrix(construct_polynomial_matrix(n, N, a*a2, X))
    print(M.dimensions())
    B = M.LLL()
    Q = sum(B[0][i]*x^i/X^i for i in range(n))
    r = Q.roots(ring=ZZ)
    if r: 
        p_maybe = r[0][0]*2**bits + a
        if N % p_maybe == 0: 
            return p_maybe