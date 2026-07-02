# Skeleton for generating the epsilon-pseudospectrum of D
import numpy as np
from scipy.linalg import svd, norm

def pseudospectrum_contour(D, epsilon=1e-2):
    # Compute the resolvent (zI - D)^-1 for a grid of complex z
    # The norm of the resolvent tells you exactly how robust your defect operator is.
    pass 
