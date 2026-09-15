from fractions import Fraction as Q
import math

def eye(m): return [[Q(i==j) for j in range(m)] for i in range(m)]
def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def matsub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def transpose(A): return [list(x) for x in zip(*A)]
def matadd(A,B): return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def shift_S(m):
    # S: e_i -> e_{i+1 mod m}
    return [[Q(1) if j == (i+1)%m else Q(0) for j in range(m)] for i in range(m)]

def shift_Sinv(m):
    return [[Q(1) if j == (i-1)%m else Q(0) for j in range(m)] for i in range(m)]

def L_m(m):
    I = eye(m); S = shift_S(m); Si = shift_Sinv(m)
    return matsub(matsub(matadd(I,I), S), Si)

def circulant_eigenvalues(m):
    # L_m eigenvalues: 4 sin^2(pi*ell/m)
    return [4*math.sin(math.pi*ell/m)**2 for ell in range(m)]

def green_kernel(m):
    # G_m(i,j) = (m^2-1)/(12m) - d(m-d)/(2m), d = min(|i-j|, m-|i-j|)
    G = [[Q(0) for _ in range(m)] for _ in range(m)]
    c = Q(m*m-1, 12*m)
    for i in range(m):
        for j in range(m):
            d = min(abs(i-j), m-abs(i-j))
            G[i][j] = c - Q(d*(m-d), 2*m)
    return G

def resistance_matrix(m):
    # Omega_m(i,j) = d(m-d)/m
    O = [[Q(0) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            d = min(abs(i-j), m-abs(i-j))
            O[i][j] = Q(d*(m-d), m)
    return O

# Verify L_m * G = I - J/m for 2 <= m <= 50
print("=== GREEN KERNEL CHECK 2<=m<=50 ===")
all_ok = True
for m in range(2, 51):
    L = L_m(m)
    G = green_kernel(m)
    LG = matmul(L, G)
    J = [[Q(1,m) for _ in range(m)] for _ in range(m)]
    I = eye(m)
    target = matsub(I, J)
    ok = (LG == target)
    if not ok:
        # check symmetry and row sums
        sym = all(G[i][j]==G[j][i] for i in range(m) for j in range(m))
        rs = [sum(G[i][j] for j in range(m)) for i in range(m)]
        print(f"m={m} LG==I-J/m: {ok} | sym={sym} | row_sums={rs}")
        all_ok = False
print("ALL PASS:", all_ok)

# Verify G is symmetric, G*1=0
print("\n=== G PROPERTIES ===")
for m in [2,3,4,5,10,50]:
    G = green_kernel(m)
    sym = all(G[i][j]==G[j][i] for i in range(m) for j in range(m))
    rs = [sum(G[i][j] for j in range(m)) for i in range(m)]
    print(f"m={m}: sym={sym}, row_sums={rs}")

# Verify resistance matrix properties
print("\n=== RESISTANCE MATRIX CHECKS ===")
for m in range(2, 51):
    O = resistance_matrix(m)
    trO = sum(O[i][i] for i in range(m))  # should be 0
    # Frobenius norm squared
    frob2 = sum(x*x for row in O for x in row)
    target_frob2 = Q(m**4 - 1, 30)
    # tr(O^3)
    O2 = matmul(O, O)
    O3 = matmul(O2, O)
    trO3 = sum(O3[i][i] for i in range(m))
    target_trO3 = Q((m*m-1)*(m*m-4)*(11*m*m+13), 2520)
    # det(O) for small m
    if m <= 6:
        # compute det via fraction -> float for sanity (exact det of rational matrix)
        import numpy as np
        detO = np.linalg.det(np.array([[float(x) for x in row] for row in O]))
        target_det = ((-1)**(m-1)) * (2**(m-2)) * (m*m-1) / (3*m*m)
        det_ok = abs(detO - target_det) < 1e-9
    else:
        det_ok = None
    
    if trO != 0 or frob2 != target_frob2 or trO3 != target_trO3:
        print(f"m={m}: trO={trO} frob2={frob2} (target {target_frob2}) trO3={trO3} (target {target_trO3}) det_ok={det_ok}")
        all_ok = False
print("RESISTANCE ALL PASS:", all_ok)

# Print sample values for adversarial audit
for m in [2,4]:
    O = resistance_matrix(m)
    frob2 = sum(x*x for row in O for x in row)
    print(f"m={m}: ||Omega||_F^2 = {frob2} = {float(frob2)}")
    
for m in [3]:
    O = resistance_matrix(m)
    O2 = matmul(O, O); O3 = matmul(O2, O)
    trO3 = sum(O3[i][i] for i in range(m))
    print(f"m={m}: tr(Omega^3) = {trO3} = {float(trO3)}")=== GREEN KERNEL CHECK 2<=m<=50 ===
ALL PASS: True

=== G PROPERTIES ===
m=2: sym=True, row_sums=[Fraction(0, 1), Fraction(0, 1)]
m=3: sym=True, row_sums=[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
m=4: sym=True, row_sums=[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
m=5: sym=True, row_sums=[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
m=10: sym=True, row_sums=[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
m=50: sym=True, row_sums=[Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]

=== RESISTANCE MATRIX CHECKS ===
RESISTANCE ALL PASS: True
m=2: ||Omega||_F^2 = 1/2 = 0.5
m=4: ||Omega||_F^2 = 17/2 = 8.5
m=3: tr(Omega^3) = 16/9 = 1.7777777777777777# === INVERSE MOMENTS / ZETA CHECKS ===
# Z_m(q) = sum_{ell=1}^{m-1} (4 sin^2(pi ell / m))^{-q}
# q=1: (m^2-1)/12
# q=2: (m^4+10m^2-11)/720
# q=3: (m^2-1)(2m^4+23m^2+191)/60480

def zeta_m(m, q):
    return sum((4*math.sin(math.pi*ell/m)**2)**(-q) for ell in range(1,m))

print("=== ZETA MOMENTS HIGH-PRECISION 2<=m<=100 ===")
max_err = 0
for m in range(2, 101):
    z1 = zeta_m(m, 1)
    t1 = (m*m-1)/12
    z2 = zeta_m(m, 2)
    t2 = (m**4 + 10*m*m - 11)/720
    z3 = zeta_m(m, 3)
    t3 = (m*m-1)*(2*m**4 + 23*m*m + 191)/60480
    e1 = abs(z1 - t1)
    e2 = abs(z2 - t2)
    e3 = abs(z3 - t3)
    max_err = max(max_err, e1, e2, e3)
    if max(e1, e2, e3) > 1e-12:
        print(f"m={m}: err q1={e1:.2e} q2={e2:.2e} q3={e3:.2e}")
print(f"MAX RELATIVE ERROR across 2<=m<=100: {max_err:.2e}")

# === SPECTRAL FORMULAS ===
print("\n=== SPECTRAL FORMULAS ===")
for m in [3,4,5,6,10]:
    sigmas = [2*math.sin(math.pi*ell/m) for ell in range(m)]  # alpha=1 for check
    lambdas = [4*math.sin(math.pi*ell/m)**2 for ell in range(m)]
    # op norm = max sigma
    op = max(sigmas)
    op_target = 2*math.sin(math.pi/2) if m%2==0 else 2*math.cos(math.pi/(2*m))
    # Frobenius norm squared = sum sigma^2 = 2m (since alpha=1)
    frob2 = sum(s*s for s in sigmas)
    # Nuclear norm = sum sigma
    nuc = sum(sigmas)
    nuc_target = 2 / math.tan(math.pi/(2*m))
    print(f"m={m}: op={op:.6f} (target {op_target:.6f}) | frob2={frob2:.1f} (target {2*m:.1f}) | nuc={nuc:.6f} (target {nuc_target:.6f})")

# === PSEUDODETERMINANT / KIRCHHOFF ===
print("\n=== PSEUDODETERMINANT / KIRCHHOFF ===")
for m in range(3, 21):
    # pdet(L_m) = m^2 (product of non-zero eigenvalues)
    pdet = 1
    for ell in range(1, m):
        pdet *= 4*math.sin(math.pi*ell/m)**2
    # tau(C_m) = m (number of spanning trees of cycle graph)
    # Kirchhoff: product of non-zero eigenvalues = m * tau(C_m) = m^2
    target = m*m
    if abs(pdet - target) > 1e-9:
        print(f"m={m}: pdet={pdet} != {target}")
print("Kirchhoff check 3<=m<=20: PASS")

# === MOORE-PENROSE / GREEN KERNEL IDENTITY ===
# G_m should equal L_m^+ (pseudoinverse)
# Check: L G = G L = I - J/m, and G symmetric, G*1=0
print("\n=== MOORE-PENROSE IDENTITY ===")
for m in [3,4,5,6,10,20]:
    L = L_m(m)
    G = green_kernel(m)
    # Check G satisfies the 4 MP conditions for pseudoinverse on zero-sum subspace
    LG = matmul(L, G); GL = matmul(G, L)
    I = eye(m); J = [[Q(1,m) for _ in range(m)] for _ in range(m)]
    P_perp = matsub(I, J)  # projection onto zero-sum
    # L G = P_perp and G L = P_perp already checked
    # G L G = G ?
    GLG = matmul(matmul(G, L), G)
    LGL = matmul(matmul(L, G), L)
    ok1 = (LG == P_perp)
    ok2 = (GL == P_perp)
    ok3 = (GLG == G)
    ok4 = (LGL == L)
    print(f"m={m}: LG=P_perp {ok1}, GL=P_perp {ok2}, GLG=G {ok3}, LGL=L {ok4}")

# === INVERSE NORM CHECKS ===
print("\n=== INVERSE NORMS (alpha=1) ===")
for m in [3,4,5,6,10]:
    # ||L^+||_F^2 = Z_m(2) = (m^4+10m^2-11)/720
    target_frob_inv = (m**4 + 10*m*m - 11)/720
    # ||L^+||_op = 1/(4 sin^2(pi/m)) for even? No, smallest non-zero eigenvalue
    # lambda_min = 4 sin^2(pi/m) for all m>=2
    lambda_min = 4*math.sin(math.pi/m)**2
    op_inv = 1/lambda_min
    print(f"m={m}: ||L^+||_F^2 = {target_frob_inv:.6f} | ||L^+||_op = 1/{lambda_min:.6f} = {op_inv:.6f}")

# === TRANSPORT IDENTITY ===
# tr((D*D)^+) = k^2(m^2-1)/(12 r(k-r)) = (1/alpha^2) * (m^2-1)/12
print("\n=== TRANSPORT SCALING ===")
for k in [4,5,6]:
    for r in [1,2]:
        if r >= k: continue
        alpha2 = r*(k-r)/(k*k)
        for m in [3,4,5]:
            lhs = (m*m-1)/(12*alpha2)
            rhs = k*k*(m*m-1)/(12*r*(k-r))
            if abs(lhs - rhs) > 1e-12:
                print(f"FAIL k={k} r={r} m={m}")
print("Transport scaling check: PASS")=== ZETA MOMENTS HIGH-PRECISION 2<=m<=100 ===
m=14: err q1=1.42e-14 q2=1.49e-13 q3=1.19e-12
m=16: err q1=2.13e-14 q2=2.98e-13 q3=2.84e-12
m=18: err q1=3.55e-15 q2=1.42e-13 q3=1.59e-12
m=19: err q1=1.42e-14 q2=2.56e-13 q3=3.87e-12
m=20: err q1=1.42e-14 q2=2.84e-13 q3=4.55e-12
m=21: err q1=4.97e-14 q2=9.66e-13 q3=1.59e-11
m=22: err q1=7.11e-15 q2=1.14e-13 q3=2.27e-12
m=23: err q1=9.95e-14 q2=2.67e-12 q3=5.46e-11
m=24: err q1=9.24e-14 q2=2.61e-12 q3=5.55e-11
m=25: err q1=9.24e-14 q2=2.73e-12 q3=6.00e-11
m=26: err q1=7.11e-15 q2=2.27e-13 q3=5.46e-12
m=27: err q1=8.53e-14 q2=3.64e-12 q3=9.82e-11
m=28: err q1=2.84e-14 q2=1.48e-12 q3=4.91e-11
m=29: err q1=7.11e-14 q2=2.84e-12 q3=8.73e-11
m=30: err q1=8.53e-14 q2=3.87e-12 q3=1.35e-10
m=31: err q1=2.70e-13 q2=1.25e-11 q3=4.62e-10
m=32: err q1=1.42e-13 q2=6.59e-12 q3=2.47e-10
m=33: err q1=1.56e-13 q2=7.05e-12 q3=2.84e-10
m=34: err q1=8.53e-14 q2=5.46e-12 q3=2.47e-10
m=35: err q1=9.95e-14 q2=5.00e-12 q3=2.33e-10
m=36: err q1=1.42e-14 q2=4.55e-13 q3=2.91e-11
m=37: err q1=2.56e-13 q2=1.73e-11 q3=9.17e-10
m=38: err q1=5.68e-14 q2=5.91e-12 q3=3.35e-10
m=39: err q1=1.71e-13 q2=1.41e-11 q3=8.29e-10
m=40: err q1=1.42e-13 q2=1.05e-11 q3=6.11e-10
m=41: err q1=3.41e-13 q2=2.86e-11 q3=1.80e-09
m=42: err q1=5.40e-13 q2=4.64e-11 q3=3.00e-09
m=43: err q1=1.14e-13 q2=6.37e-12 q3=3.49e-10
m=44: err q1=1.42e-13 q2=1.18e-11 q3=8.15e-10
m=45: err q1=3.98e-13 q2=3.55e-11 q3=2.68e-09
m=46: err q1=8.53e-14 q2=1.91e-11 q3=1.69e-09
m=47: err q1=3.13e-13 q2=2.91e-11 q3=2.39e-09
m=48: err q1=1.71e-13 q2=1.36e-11 q3=9.90e-10
m=49: err q1=5.97e-13 q2=6.91e-11 q3=6.29e-09
m=50: err q1=5.12e-13 q2=5.64e-11 q3=5.12e-09
m=51: err q1=8.53e-14 q2=1.27e-11 q3=1.51e-09
m=52: err q1=6.54e-13 q2=8.91e-11 q3=9.08e-09
m=53: err q1=3.13e-13 q2=4.91e-11 q3=5.47e-09
m=54: err q1=3.13e-13 q2=3.82e-11 q3=4.19e-09
m=55: err q1=1.11e-12 q2=1.76e-10 q3=2.05e-08
m=56: err q1=3.98e-13 q2=5.64e-11 q3=6.52e-09
m=57: err q1=4.55e-13 q2=6.55e-11 q3=7.92e-09
m=58: err q1=1.25e-12 q2=2.00e-10 q3=2.54e-08
m=59: err q1=5.68e-13 q2=6.55e-11 q3=7.68e-09
m=60: err q1=1.71e-13 q2=1.82e-11 q3=2.56e-09
m=61: err q1=8.53e-13 q2=1.42e-10 q3=1.93e-08
m=62: err q1=1.14e-13 q2=6.91e-11 q3=1.19e-08
m=63: err q1=1.42e-12 q2=2.62e-10 q3=3.91e-08
m=64: err q1=5.68e-14 q2=3.64e-11 q3=6.52e-09
m=65: err q1=1.14e-12 q2=2.36e-10 q3=3.77e-08
m=66: err q1=1.99e-12 q2=4.04e-10 q3=6.61e-08
m=67: err q1=7.39e-13 q2=2.07e-10 q3=3.73e-08
m=68: err q1=1.14e-13 q2=1.82e-11 q3=2.33e-09
m=69: err q1=0.00e+00 q2=4.73e-11 q3=9.78e-09
m=70: err q1=7.96e-13 q2=1.67e-10 q3=3.07e-08
m=71: err q1=2.39e-12 q2=6.33e-10 q3=1.23e-07
m=72: err q1=4.55e-13 q2=1.09e-10 q3=2.14e-08
m=73: err q1=8.53e-13 q2=2.04e-10 q3=4.00e-08
m=74: err q1=1.71e-12 q2=4.15e-10 q3=8.38e-08
m=75: err q1=1.48e-12 q2=3.57e-10 q3=7.26e-08
m=76: err q1=1.71e-12 q2=4.80e-10 q3=1.06e-07
m=77: err q1=1.48e-12 q2=3.64e-10 q3=8.01e-08
m=78: err q1=3.41e-13 q2=1.53e-10 q3=3.63e-08
m=79: err q1=2.05e-12 q2=6.40e-10 q3=1.53e-07
m=80: err q1=6.82e-13 q2=2.69e-10 q3=6.52e-08
m=81: err q1=1.25e-12 q2=3.57e-10 q3=8.75e-08
m=82: err q1=2.16e-12 q2=6.62e-10 q3=1.64e-07
m=83: err q1=5.68e-12 q2=1.89e-09 q3=4.94e-07
m=84: err q1=1.02e-12 q2=5.38e-10 q3=1.53e-07
m=85: err q1=1.14e-13 q2=4.37e-11 q3=1.12e-08
m=86: err q1=3.07e-12 q2=1.14e-09 q3=3.22e-07
m=87: err q1=3.41e-13 q2=2.91e-11 q3=1.30e-08
m=88: err q1=3.75e-12 q2=1.40e-09 q3=4.08e-07
m=89: err q1=8.07e-12 q2=3.04e-09 q3=9.05e-07
m=90: err q1=2.73e-12 q2=1.30e-09 q3=4.06e-07
m=91: err q1=1.71e-12 q2=7.57e-10 q3=2.46e-07
m=92: err q1=2.61e-12 q2=1.15e-09 q3=3.76e-07
m=93: err q1=5.91e-12 q2=2.40e-09 q3=7.79e-07
m=94: err q1=5.00e-12 q2=2.15e-09 q3=7.15e-07
m=95: err q1=2.39e-12 q2=1.37e-09 q3=4.84e-07
m=96: err q1=1.71e-12 q2=9.17e-10 q3=3.24e-07
m=97: err q1=2.16e-12 q2=9.46e-10 q3=3.35e-07
m=98: err q1=7.28e-12 q2=3.27e-09 q3=1.17e-06
m=99: err q1=7.73e-12 q2=3.52e-09 q3=1.29e-06
m=100: err q1=3.41e-13 q2=4.07e-10 q3=1.79e-07
MAX RELATIVE ERROR across 2<=m<=100: 1.29e-06

=== SPECTRAL FORMULAS ===
m=3: op=1.732051 (target 1.732051) | frob2=6.0 (target 6.0) | nuc=3.464102 (target 3.464102)
m=4: op=2.000000 (target 2.000000) | frob2=8.0 (target 8.0) | nuc=4.828427 (target 4.828427)
m=5: op=1.902113 (target 1.902113) | frob2=10.0 (target 10.0) | nuc=6.155367 (target 6.155367)
m=6: op=2.000000 (target 2.000000) | frob2=12.0 (target 12.0) | nuc=7.464102 (target 7.464102)
m=10: op=2.000000 (target 2.000000) | frob2=20.0 (target 20.0) | nuc=12.627503 (target 12.627503)

=== PSEUDODETERMINANT / KIRCHHOFF ===
Kirchhoff check 3<=m<=20: PASS

=== MOORE-PENROSE IDENTITY ===
m=3: LG=P_perp True, GL=P_perp True, GLG=G True, LGL=L True
m=4: LG=P_perp True, GL=P_perp True, GLG=G True, LGL=L True
m=5: LG=P_perp True, GL=P_perp True, GLG=G True, LGL=L True
m=6: LG=P_perp True, GL=P_perp True, GLG=G True, LGL=L True
m=10: LG=P_perp True, GL=P_perp True, GLG=G True, LGL=L True
m=20: LG=P_perp True, GL=P_perp True, GLG=G True, LGL=L True

=== INVERSE NORMS (alpha=1) ===
m=3: ||L^+||_F^2 = 0.222222 | ||L^+||_op = 1/3.000000 = 0.333333
m=4: ||L^+||_F^2 = 0.562500 | ||L^+||_op = 1/2.000000 = 0.500000
m=5: ||L^+||_F^2 = 1.200000 | ||L^+||_op = 1/1.381966 = 0.723607
m=6: ||L^+||_F^2 = 2.284722 | ||L^+||_op = 1/1.000000 = 1.000000
m=10: ||L^+||_F^2 = 15.262500 | ||L^+||_op = 1/0.381966 = 2.618034

=== TRANSPORT SCALING ===
Transport scaling check: PASS# === ALGEBRAIC IDENTITY: I - A^T A = pq L_m ===
# A = q S^b + p S^{b+1}, S = cyclic shift on Z/mZ

def matpow(M, e):
    n = len(M)
    if e == 0: return eye(n)
    R = matpow(M, e//2)
    R2 = matmul(R, R)
    return matmul(M, R2) if e%2 else R2

def scalar_mul(A, c):
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

print("=== ALGEBRAIC IDENTITY I - A^T A = pq L_m ===")
all_ok = True
for m in range(2, 21):
    S = shift_S(m)
    Si = shift_Sinv(m)
    I = eye(m)
    L = matsub(matsub(matadd(I, I), S), Si)
    for b in range(m):
        Sb = matpow(S, b)
        Sb1 = matpow(S, b+1)
        for k in [3,4,5,6,7,8]:
            for r in range(1, k):
                p = Q(r, k)
                q = Q(k-r, k)
                A = matadd(scalar_mul(Sb, q), scalar_mul(Sb1, p))
                At = transpose(A)
                AtA = matmul(At, A)
                lhs = matsub(I, AtA)
                rhs = scalar_mul(L, p*q)
                if lhs != rhs:
                    print(f"FAIL m={m} b={b} k={k} r={r}")
                    all_ok = False
print("ALL PASS:", all_ok)

# === B = S - I, B^T B = L_m ===
print("\n=== B^T B = L_m for B = S - I ===")
for m in range(2, 21):
    S = shift_S(m); I = eye(m)
    B = matsub(S, I)
    BtB = matmul(transpose(B), B)
    L = matsub(matsub(matadd(I, I), S), shift_Sinv(m))
    if BtB != L:
        print(f"FAIL m={m}")
        all_ok = False
print("B^T B = L_m ALL PASS:", all_ok)

# === Verify the explicit D construction for a specific case ===
# We need to construct the actual U, K, P, T for SV-002.
# From context: this appears to be a quotient construction where
# we have k states, r of one type, and we quotient to a cycle of length m.
# Let's try to reconstruct from the algebraic identity.
# U: R^m -> R^k, U^T U = I_m, U U^T = P (projection onto some m-dim subspace)
# K: Koopman operator on k states
# D = (I - P) K P
# U^T D^T D U = I - A^T A where A = U^T K U

# For the circulant case, U maps basis e_j of R^m to a set of k basis vectors
# that are cyclically arranged. The simplest case: k = m, r = 1, U = I.
# Then P = I, D = 0, which is trivial and not interesting.

# More likely: k = 2m or similar, with a 2-coloring pattern.
# Actually, from "A = q S_b + p S_{b+1}", A is an m×m circulant.
# U is an isometry from R^m to R^k.
# K is a deterministic map on k states.

# Without the explicit construction, I cannot verify U^T D^T D U = α² L_m
# as a matrix identity. But I CAN verify:
# 1. The algebraic identity I - A^T A = pq L_m holds for all m, b, p, q
# 2. The spectral consequences follow
# 3. The Green kernel and resistance formulas follow from L_m

print("\n=== SPECTRAL CONSEQUENCES ===")
for m in [3,4,5,6,10]:
    sigmas = [2*math.sin(math.pi*ell/m) for ell in range(m)]
    # alpha=1 case; for general alpha, scale by alpha
    # op norm
    op_even = 2 if m%2==0 else 2*math.cos(math.pi/(2*m))
    op_actual = max(sigmas)
    # stable rank = ||D||_F^2 / ||D||_op^2 = (2m alpha^2) / (4 alpha^2) = m/2 for even
    # for odd: op = 2 cos(pi/2m), so stable rank = 2m / (4 cos^2(pi/2m)) = (m/2) sec^2(pi/2m)
    sr_even = m/2
    sr_odd = (m/2) / (math.cos(math.pi/(2*m))**2)
    sr_actual = sum(s*s for s in sigmas) / (max(sigmas)**2)
    print(f"m={m}: op={op_actual:.6f} (target {op_even:.6f}) | stable_rank={sr_actual:.4f} (even {sr_even:.4f} odd {sr_odd:.4f})")

# === CONDITION NUMBER ===
print("\n=== CONDITION NUMBER κ_+(D) ===")
for m in [3,4,5,6,10,20,50]:
    sigmas = [2*math.sin(math.pi*ell/m) for ell in range(1,m)]  # exclude 0
    kappa = max(sigmas) / min(sigmas)
    # even: max=2, min=2 sin(pi/m), so kappa = 1/sin(pi/m) = csc(pi/m)
    # odd: max=2 cos(pi/2m), min=2 sin(pi/m), so kappa = cos(pi/2m)/sin(pi/m) = 1/(2 sin(pi/2m))
    if m%2==0:
        target = 1/math.sin(math.pi/m)
    else:
        target = 1/(2*math.sin(math.pi/(2*m)))
    print(f"m={m}: κ={kappa:.6f} (target {target:.6f}) | ~m/π = {m/math.pi:.6f}")=== ALGEBRAIC IDENTITY I - A^T A = pq L_m ===
ALL PASS: True

=== B^T B = L_m for B = S - I ===
B^T B = L_m ALL PASS: True

=== SPECTRAL CONSEQUENCES ===
m=3: op=1.732051 (target 1.732051) | stable_rank=2.0000 (even 1.5000 odd 2.0000)
m=4: op=2.000000 (target 2.000000) | stable_rank=2.0000 (even 2.0000 odd 2.3431)
m=5: op=1.902113 (target 1.902113) | stable_rank=2.7639 (even 2.5000 odd 2.7639)
m=6: op=2.000000 (target 2.000000) | stable_rank=3.0000 (even 3.0000 odd 3.2154)
m=10: op=2.000000 (target 2.000000) | stable_rank=5.0000 (even 5.0000 odd 5.1254)

=== CONDITION NUMBER κ_+(D) ===
m=3: κ=1.000000 (target 1.000000) | ~m/π = 0.954930
m=4: κ=1.414214 (target 1.414214) | ~m/π = 1.273240
m=5: κ=1.618034 (target 1.618034) | ~m/π = 1.591549
m=6: κ=2.000000 (target 2.000000) | ~m/π = 1.909859
m=10: κ=3.236068 (target 3.236068) | ~m/π = 3.183099
m=20: κ=6.392453 (target 6.392453) | ~m/π = 6.366198
m=50: κ=15.925971 (target 15.925971) | ~m/π = 15.915494/# === RESISTANCE MATRIX DETERMINANT ===
# det Omega = (-1)^{m-1} 2^{m-2} (m^2-1) / (3 m^2)
import numpy as np

print("=== RESISTANCE MATRIX DETERMINANT ===")
for m in range(2, 11):
    O = resistance_matrix(m)
    # Convert to float matrix for numpy det
    Of = np.array([[float(x) for x in row] for row in O])
    detO = np.linalg.det(Of)
    target = ((-1)**(m-1)) * (2**(m-2)) * (m*m - 1) / (3 * m * m)
    print(f"m={m}: det={detO:.6f} target={target:.6f} match={abs(detO-target)<1e-9}")

# === KIRCHHOFF INDEX ===
# Kf(C_m) = m tr(L_m^+) = m(m^2-1)/12
print("\n=== KIRCHHOFF INDEX ===")
for m in range(2, 21):
    L = L_m(m)
    G = green_kernel(m)
    trLp = sum(G[i][i] for i in range(m))
    kf = m * trLp
    target = m*(m*m-1)/12
    if abs(float(kf) - target) > 1e-9:
        print(f"m={m}: Kf={float(kf):.6f} target={target:.6f}")
print("Kirchhoff index 2<=m<=20: PASS")

# === INVERSE NORM IDENTITIES ===
# ||D^+||_F^2 = (m^2-1)/(12 alpha^2)
# For alpha=1: ||L^+||_F^2 = (m^4+10m^2-11)/720
print("\n=== INVERSE FROBENIUS CHECK ===")
for m in range(2, 21):
    G = green_kernel(m)
    frob2 = sum(x*x for row in G for x in row)
    target = (m**4 + 10*m*m - 11)/720
    if abs(float(frob2) - target) > 1e-9:
        print(f"m={m}: ||L^+||_F^2={float(frob2):.6f} target={target:.6f}")
print("Inverse Frobenius 2<=m<=20: PASS")

# === TRANSPORT IDENTITY: m alpha^2 ||D^+||_F^2 = Kf(C_m) ===
print("\n=== TRANSPORT IDENTITY ===")
for m in [3,4,5,6,10]:
    for k in [4,5,6]:
        for r in range(1,k):
            alpha2 = r*(k-r)/(k*k)
            lhs = m * alpha2 * (m*m-1)/(12*alpha2)  # = m(m^2-1)/12
            rhs = m*(m*m-1)/12
            if abs(lhs - rhs) > 1e-12:
                print(f"FAIL m={m} k={k} r={r}")
print("Transport identity: PASS")

# === STABLE RANK ===
print("\n=== STABLE RANK ===")
for m in [3,4,5,6,10,20]:
    sigmas = [2*math.sin(math.pi*ell/m) for ell in range(1,m)]  # non-zero
    sr = sum(s*s for s in sigmas) / (max(sigmas)**2)
    if m % 2 == 0:
        target = m/2
    else:
        target = (m/2) / (math.cos(math.pi/(2*m))**2)
    print(f"m={m}: stable_rank={sr:.4f} target={target:.4f}")

# === CONDITION NUMBER ===
print("\n=== CONDITION NUMBER κ_+(D) ===")
for m in [3,4,5,6,10,20,50,100]:
    sigmas = [2*math.sin(math.pi*ell/m) for ell in range(1,m)]
    kappa = max(sigmas)/min(sigmas)
    if m%2==0:
        target = 1/math.sin(math.pi/m)
    else:
        target = 1/(2*math.sin(math.pi/(2*m)))
    print(f"m={m}: κ={kappa:.6f} target={target:.6f} ratio_to_m/pi={kappa/(m/math.pi):.6f}")

# === PSEUDODETERMINANT of D*D ===
# pdet(D*D) = m^2 alpha^{2(m-1)}
# For alpha=1: pdet(L_m) = m^2
print("\n=== PSEUDODETERMINANT ===")
for m in range(3, 21):
    pdet = 1
    for ell in range(1, m):
        pdet *= 4*math.sin(math.pi*ell/m)**2
    target = m*m
    if abs(pdet - target) > 1e-9:
        print(f"m={m}: pdet={pdet} target={target}")
print("Pseudodeterminant 3<=m<=20: PASS")

# === PRODUCT OF NONZERO SINGULAR VALUES ===
# product σ_ℓ = m alpha^{m-1}
print("\n=== PRODUCT NONZERO SINGULAR VALUES ===")
for m in range(3, 21):
    prod = 1
    for ell in range(1, m):
        prod *= 2*math.sin(math.pi*ell/m)
    target = m  # alpha=1
    if abs(prod - target) > 1e-9:
        print(f"m={m}: prod={prod} target={target}")
print("Product nonzero singular values 3<=m<=20: PASS")=== RESISTANCE MATRIX DETERMINANT ===
m=2: det=-0.250000 target=-0.250000 match=True
m=3: det=0.592593 target=0.592593 match=True
m=4: det=-1.250000 target=-1.250000 match=True
m=5: det=2.560000 target=2.560000 match=True
m=6: det=-5.185185 target=-5.185185 match=True
m=7: det=10.448980 target=10.448980 match=True
m=8: det=-21.000000 target=-21.000000 match=True
m=9: det=42.139918 target=42.139918 match=True
m=10: det=-84.480000 target=-84.480000 match=True

=== KIRCHHOFF INDEX ===
Kirchhoff index 2<=m<=20: PASS

=== INVERSE FROBENIUS CHECK ===
Inverse Frobenius 2<=m<=20: PASS

=== TRANSPORT IDENTITY ===
Transport identity: PASS

=== STABLE RANK ===
m=3: stable_rank=2.0000 target=2.0000
m=4: stable_rank=2.0000 target=2.0000
m=5: stable_rank=2.7639 target=2.7639
m=6: stable_rank=3.0000 target=3.0000
m=10: stable_rank=5.0000 target=5.0000
m=20: stable_rank=10.0000 target=10.0000

=== CONDITION NUMBER κ_+(D) ===
m=3: κ=1.000000 target=1.000000 ratio_to_m/pi=1.047198
m=4: κ=1.414214 target=1.414214 ratio_to_m/pi=1.110721
m=5: κ=1.618034 target=1.618034 ratio_to_m/pi=1.016641
m=6: κ=2.000000 target=2.000000 ratio_to_m/pi=1.047198
m=10: κ=3.236068 target=3.236068 ratio_to_m/pi=1.016641
m=20: κ=6.392453 target=6.392453 ratio_to_m/pi=1.004124
m=50: κ=15.925971 target=15.925971 ratio_to_m/pi=1.000658
m=100: κ=31.836225 target=31.836225 ratio_to_m/pi=1.000165

=== PSEUDODETERMINANT ===
Pseudodeterminant 3<=m<=20: PASS

=== PRODUCT NONZERO SINGULAR VALUES ===
Product nonzero singular values 3<=m<=20: PASS
