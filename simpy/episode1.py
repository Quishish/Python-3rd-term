import sympy as sp


rho, lam, mu = sp.symbols("rho lambda mu")
A = sp.zeros(9)
for i in range(3):
    A[i, i + 3] = -1 / rho
A[3, 0] = -(lam + 2 * mu)
A[4, 1] = -mu
A[5, 2] = -mu
A[6, 0] = -lam
A[8, 0] = -lam

print("Eigenvalues and multiplicities:")
for value, count in A.eigenvals().items():
    print(value, "-", count)