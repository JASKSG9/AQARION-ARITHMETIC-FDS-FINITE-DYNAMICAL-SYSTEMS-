from fractions import Fraction as Q

def det2(A):
    return A[0][0]*A[1][1] - A[0][1]*A[1][0]

def charpoly_2x2(A):
    tr = A[0][0] + A[1][1]
    return (Q(1), -tr, det2(A))

L2 = [[Q(2), Q(-2)],
      [Q(-2), Q(2)]]

K2 = [[Q(1), Q(-1)],
      [Q(-1), Q(1)]]

# Exact fingerprints
assert L2!= K2
assert charpoly_2x2(L2) == (Q(1), Q(-4), Q(0)), "L2 spectrum {0,4}"
assert charpoly_2x2(K2) == (Q(1), Q(-2), Q(0)), "K2 spectrum {0,2}"
# SimpleGraph.Cycle interpretation REJECTED for m=2, multigraph ACCEPTED
