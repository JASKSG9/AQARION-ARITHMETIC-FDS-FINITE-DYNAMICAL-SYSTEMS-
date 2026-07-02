# 4. Spectral Fine‑Structure
python -c "
import numpy as np
from aqarion_core_final import GapQuotientSystem
sys = GapQuotientSystem(10,4)
A = np.zeros((54,54), int)
for i,g in enumerate(sys.G):
    j = sys.state_to_idx[sys.T_G[g]]
    A[i,j] = 1
vals = np.linalg.eigvals(A)
print('Unique eigenvalues:', sorted(set(np.round(vals,10))))
"
# Expect: only {0,1}. Any other value → BREAKTHROUGH.

# 5. Nilpotent Rank Sequence
python -c "
import numpy as np
...
N = A - np.eye(54) * 0  # adjust for attractor
for k in range(1,8):
    r = np.linalg.matrix_rank(np.linalg.matrix_power(N,k))
    print(f'rank(N^{k}) = {r}')
"
# Should strictly decrease to 0 at k=7.

# 6. Collapse‑Radius Ultrametric Check
python -c "
import numpy as np
R = np.load('phase_a2_radius_matrix.npy')
n = R.shape[0]
violations = 0
for i in range(n):
    for j in range(n):
        for k in range(n):
            if R[i,j]>=0 and R[j,k]>=0 and R[i,k]>=0:
                if R[i,k] > max(R[i,j], R[j,k]):
                    violations += 1
print('Ultrametric violations:', violations)
"
# If zero, the synchronization metric is an ultrametric – a strong hidden structure.
