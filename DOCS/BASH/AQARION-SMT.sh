# 1. SMT Infinite Counterexample Search
python DOCS/PYTHON/EXAMPLES/SMT-COUNTER-EXAMPLE.py
# Expected: generates Z3 models proving D=0 ≠> C=0 for n≥4.
# Breakthrough: if Z3 fails to find a model, the Commutator Fallacy might be false for some n.

# 2. Partition Lattice Laplacian
python DOCS/PYTHON/LAPLACIAN.py
# Computes Fiedler eigenvalue for the 54-state quotient.
# Breakthrough: unusually large or small Fiedler value would indicate a critical bottleneck
# or near‑decoupling of the refinement space.

# 3. Pseudospectral Analysis of Defect Operator
python ARTIFACTS/PSEUDOSPECTRAL_d.py
# Plots ε‑pseudospectrum of the integer defect matrix.
# Breakthrough: if pseudospectral abscissa > spectral radius, the defect is highly non‑normal,
# implying large transient error amplification under partition perturbation.

---

python DOCS/PYTHON/EXAMPLES/SMT-COUNTER-EXAMPLE.py
python DOCS/PYTHON/LAPLACIAN.py
python ARTIFACTS/PSEUDOSPECTRAL_d.py
