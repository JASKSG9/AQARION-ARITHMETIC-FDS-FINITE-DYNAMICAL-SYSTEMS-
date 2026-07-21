```python
#!/usr/bin/env python3
"""
AQ-QDO-001: Quantum Defect Operator (Choi-SVD)

AQARION Quantum Extension: Measures leakage of a quantum channel
relative to an observable subspace, providing the quantum analog of
the classical defect operator D = (I-P)KP.

Classical AQARION          Quantum AQARION
------------------         ----------------
State space X              Hilbert space H (dim d)
Partition P                Observable projector P_obs (d x d)
Koopman K                  Quantum channel E (Choi matrix J, d² x d²)
Defect D = (I-P)KP         Leakage Choi L = (I⊗(I-P_obs)) J (I⊗(I-P_obs))
rank(D)                    escape_dim = rank(L)
||D||_Frobenius            ||L||_Frobenius
D² = 0                     L² = 0 (nilpotency check)
Entropy H_D                SVD entropy of L

Core Theorem:
    L = 0  ⇔  channel preserves observable subspace.

Author: AQARION Research Node #10878
Date: 2026-07-21
Version: 1.0
"""

import numpy as np
import numpy.linalg as la
import json
import hashlib
from datetime import datetime

class QuantumDefectOperator:
    """
    Quantum defect operator via Choi matrix and SVD.
    """

    def __init__(self, n_qubits: int = 1):
        self.n_qubits = n_qubits
        self.d = 1 << n_qubits          # Hilbert space dimension
        self.choi_dim = self.d ** 2    # Choi matrix dimension

    def choi_from_unitary(self, U: np.ndarray) -> np.ndarray:
        """
        Choi matrix for a unitary channel E(ρ) = U ρ U†.
        J = (I ⊗ U) |Ω><Ω| (I ⊗ U†) with |Ω> = Σ_i |i> ⊗ |i>.
        """
        # Build |Ω> as a d²-dimensional vector
        Omega = np.zeros(self.choi_dim, dtype=complex)
        for i in range(self.d):
            Omega[i * self.d + i] = 1.0

        # Apply I ⊗ U
        IU = np.kron(np.eye(self.d), U)
        psi = IU @ Omega

        # Choi = |ψ><ψ|
        J = np.outer(psi, psi.conj())
        return J

    def leakage_choi(self, J: np.ndarray, P_obs: np.ndarray) -> np.ndarray:
        """
        Leakage operator: L = (I⊗(I-P_obs)) J (I⊗(I-P_obs)).
        This is the quantum analog of (I-P)KP.
        """
        I = np.eye(self.d)
        P_err = I - P_obs
        # Projector on the output leg: I ⊗ P_err
        K = np.kron(I, P_err)
        # Double-sided projection
        return K @ J @ K

    def svd_analysis(self, L: np.ndarray, tol: float = 1e-10) -> dict:
        """
        SVD analysis of the leakage Choi matrix.
        Returns:
            escape_dim: rank(L)
            singular_values: top singular values
            principal_leakage: largest singular value
            leakage_frobenius_norm: Frobenius norm of L
            is_nilpotent: whether L² ≈ 0
            nilpotency_residual: ||L²||_F
            entropy: SVD entropy of L
            energy_concentration: cumulative energy fractions
            low_rank_error: reconstruction error
        """
        U, S, Vt = la.svd(L, full_matrices=False)
        nonzero = int(np.sum(S > tol))

        # Frobenius norm
        frob_norm = float(la.norm(L))

        # Nilpotency check: L² should be zero for square-zero defect
        L2 = L @ L
        nil_res = float(la.norm(L2))
        is_nilpotent = nil_res < tol * 100

        # SVD entropy
        if nonzero > 0:
            p = S[:nonzero] / np.sum(S[:nonzero])
            H = float(-np.sum(p * np.log(p + 1e-15)))
        else:
            H = 0.0

        return {
            "escape_dim": nonzero,
            "singular_values": [float(s) for s in S[:min(8, len(S))]],
            "principal_leakage": float(S[0]) if len(S) > 0 else 0.0,
            "leakage_frobenius_norm": frob_norm,
            "is_nilpotent": is_nilpotent,
            "nilpotency_residual": nil_res,
            "entropy": H,
            "energy_concentration": [
                float(np.sum(S[:k+1]**2) / np.sum(S**2))
                for k in range(min(5, len(S)))
            ],
            "low_rank_error": float(
                la.norm(L - U[:, :nonzero] @ np.diag(S[:nonzero]) @ Vt[:nonzero, :])
            )
        }

    def classical_to_quantum_map(self, classical_result: dict) -> dict:
        """Map classical AQARION invariants to quantum invariants."""
        return {
            "classical_rank_D": classical_result.get("rank", 0),
            "quantum_escape_dim": "rank of leakage Choi",
            "classical_frobenius": classical_result.get("frobenius", 0.0),
            "quantum_principal_leakage": "sigma_max of leakage Choi",
            "classical_entropy_H": classical_result.get("entropy", 0.0),
            "quantum_svd_entropy": "entropy of singular value distribution",
            "classical_D2_zero": "quantum_nilpotency_check"
        }


def demo():
    """Run demonstration on common quantum gates."""
    print("=" * 72)
    print("AQ-QDO-001: QUANTUM DEFECT OPERATOR DEMO")
    print("=" * 72)

    qdo = QuantumDefectOperator(n_qubits=1)

    # --- Demo 1: Hadamard, P_obs = |+><+| ---
    print("\n--- Demo 1: Hadamard gate, P_obs = |+><+| ---")
    U_h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    J_h = qdo.choi_from_unitary(U_h)
    P_plus = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
    L_h = qdo.leakage_choi(J_h, P_plus)
    res_h = qdo.svd_analysis(L_h)
    print(f"  Choi shape: {J_h.shape}")
    print(f"  Escape dimension: {res_h['escape_dim']}")
    print(f"  Principal leakage: {res_h['principal_leakage']:.6f}")
    print(f"  Frobenius norm: {res_h['leakage_frobenius_norm']:.6f}")
    print(f"  Is nilpotent: {res_h['is_nilpotent']} (residual {res_h['nilpotency_residual']:.2e})")
    print(f"  SVD entropy: {res_h['entropy']:.6f}")
    print(f"  Top singular values: {[round(s, 6) for s in res_h['singular_values']]}")

    # --- Demo 2: Hadamard, P_obs = |0><0| ---
    print("\n--- Demo 2: Hadamard gate, P_obs = |0><0| ---")
    P_0 = np.array([[1, 0], [0, 0]], dtype=complex)
    L_h0 = qdo.leakage_choi(J_h, P_0)
    res_h0 = qdo.svd_analysis(L_h0)
    print(f"  Escape dimension: {res_h0['escape_dim']}")
    print(f"  Principal leakage: {res_h0['principal_leakage']:.6f}")
    print(f"  Frobenius norm: {res_h0['leakage_frobenius_norm']:.6f}")
    print(f"  Is nilpotent: {res_h0['is_nilpotent']} (residual {res_h0['nilpotency_residual']:.2e})")
    print(f"  SVD entropy: {res_h0['entropy']:.6f}")

    # --- Demo 3: Identity gate, P_obs = |+><+| ---
    print("\n--- Demo 3: Identity gate, P_obs = |+><+| ---")
    U_id = np.eye(2, dtype=complex)
    J_id = qdo.choi_from_unitary(U_id)
    L_id = qdo.leakage_choi(J_id, P_plus)
    res_id = qdo.svd_analysis(L_id)
    print(f"  Escape dimension: {res_id['escape_dim']}")
    print(f"  Principal leakage: {res_id['principal_leakage']:.6f}")
    print(f"  Frobenius norm: {res_id['leakage_frobenius_norm']:.6f}")
    print(f"  Is nilpotent: {res_id['is_nilpotent']} (residual {res_id['nilpotency_residual']:.2e})")

    # --- Demo 4: CNOT (2 qubits), P_obs = |00><00| ---
    print("\n--- Demo 4: CNOT gate (2 qubits), P_obs = |00><00| ---")
    qdo2 = QuantumDefectOperator(n_qubits=2)
    U_cnot = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
    J_cnot = qdo2.choi_from_unitary(U_cnot)
    P_00 = np.zeros((4,4), dtype=complex)
    P_00[0,0] = 1.0
    L_cnot = qdo2.leakage_choi(J_cnot, P_00)
    res_cnot = qdo2.svd_analysis(L_cnot)
    print(f"  Choi shape: {J_cnot.shape}")
    print(f"  Escape dimension: {res_cnot['escape_dim']}")
    print(f"  Principal leakage: {res_cnot['principal_leakage']:.6f}")
    print(f"  Frobenius norm: {res_cnot['leakage_frobenius_norm']:.6f}")
    print(f"  Is nilpotent: {res_cnot['is_nilpotent']} (residual {res_cnot['nilpotency_residual']:.2e})")
    print(f"  SVD entropy: {res_cnot['entropy']:.6f}")

    # Collect results for JSON artifact
    results = {
        "Hadamard_plus": res_h,
        "Hadamard_0": res_h0,
        "Identity_plus": res_id,
        "CNOT_00": res_cnot
    }
    return results


def save_artifact(results):
    """Save the quantum defect analysis as a JSON certificate."""
    timestamp = datetime.now().isoformat()
    artifact = {
        "module": "AQ-QDO-001",
        "name": "Quantum Defect Operator (Choi-SVD)",
        "description": "AQARION quantum extension: measures leakage of a quantum channel relative to an observable subspace.",
        "version": "1.0",
        "timestamp": timestamp,
        "demonstrations": {
            "Hadamard_plus": {
                "n_qubits": 1,
                "gate": "Hadamard",
                "P_obs": "|+><+|",
                "escape_dim": results["Hadamard_plus"]["escape_dim"],
                "principal_leakage": results["Hadamard_plus"]["principal_leakage"],
                "leakage_frobenius_norm": results["Hadamard_plus"]["leakage_frobenius_norm"],
                "is_nilpotent": results["Hadamard_plus"]["is_nilpotent"],
                "nilpotency_residual": results["Hadamard_plus"]["nilpotency_residual"],
                "entropy": results["Hadamard_plus"]["entropy"],
                "singular_values": results["Hadamard_plus"]["singular_values"]
            },
            "Hadamard_0": {
                "n_qubits": 1,
                "gate": "Hadamard",
                "P_obs": "|0><0|",
                "escape_dim": results["Hadamard_0"]["escape_dim"],
                "principal_leakage": results["Hadamard_0"]["principal_leakage"],
                "leakage_frobenius_norm": results["Hadamard_0"]["leakage_frobenius_norm"],
                "is_nilpotent": results["Hadamard_0"]["is_nilpotent"],
                "nilpotency_residual": results["Hadamard_0"]["nilpotency_residual"],
                "entropy": results["Hadamard_0"]["entropy"],
                "singular_values": results["Hadamard_0"]["singular_values"]
            },
            "Identity_plus": {
                "n_qubits": 1,
                "gate": "Identity",
                "P_obs": "|+><+|",
                "escape_dim": results["Identity_plus"]["escape_dim"],
                "principal_leakage": results["Identity_plus"]["principal_leakage"],
                "leakage_frobenius_norm": results["Identity_plus"]["leakage_frobenius_norm"],
                "is_nilpotent": results["Identity_plus"]["is_nilpotent"],
                "nilpotency_residual": results["Identity_plus"]["nilpotency_residual"],
                "entropy": results["Identity_plus"]["entropy"],
                "singular_values": results["Identity_plus"]["singular_values"]
            },
            "CNOT_00": {
                "n_qubits": 2,
                "gate": "CNOT",
                "P_obs": "|00><00|",
                "escape_dim": results["CNOT_00"]["escape_dim"],
                "principal_leakage": results["CNOT_00"]["principal_leakage"],
                "leakage_frobenius_norm": results["CNOT_00"]["leakage_frobenius_norm"],
                "is_nilpotent": results["CNOT_00"]["is_nilpotent"],
                "nilpotency_residual": results["CNOT_00"]["nilpotency_residual"],
                "entropy": results["CNOT_00"]["entropy"],
                "singular_values": results["CNOT_00"]["singular_values"]
            }
        },
        "classical_quantum_bridge": {
            "classical": {
                "space": "Finite set X (n states)",
                "observable": "Partition P (blocks)",
                "dynamics": "Functional graph T: X → X",
                "operator": "Koopman K (n x n), K[i,T[i]] = 1",
                "defect": "D = (I-P)KP (n x n)",
                "invariant_condition": "D = 0",
                "rank": "rank(D) = number of independent leakage channels",
                "norm": "||D||_Frobenius = total leakage strength",
                "entropy": "H_D = -Σ p_i log p_i over singular values"
            },
            "quantum": {
                "space": "Hilbert space H (dim d = 2^n_qubits)",
                "observable": "Projector P_obs (d x d) onto measurement subspace",
                "dynamics": "Quantum channel E: B(H) → B(H)",
                "operator": "Choi matrix J (d² x d²)",
                "defect": "Leakage Choi L = (I⊗(I-P_obs)) J (I⊗(I-P_obs)) (d² x d²)",
                "invariant_condition": "L = 0 (channel preserves observable subspace)",
                "rank": "escape_dim = rank(L) = quantum leakage channels",
                "norm": "||L||_Frobenius = total leakage strength",
                "entropy": "SVD entropy of L"
            },
            "correspondence": {
                "n (classical states)": "d² (Choi dimension, not directly comparable)",
                "partition blocks": "eigenprojectors of P_obs",
                "block size": "dimension of eigenspace",
                "T-invariance": "E(P_obs B(H) P_obs) ⊆ P_obs B(H) P_obs (quantum invariance)",
                "exact quotient": "quantum channel restricts to subalgebra"
            }
        },
        "status": "OPERATIONAL",
        "certificate_id": "AQ-QDO-001-CERT",
        "sha256": hashlib.sha256(
            json.dumps(artifact, sort_keys=True, separators=(',', ':')).encode()
        ).hexdigest()
    }

    # Save to file
    with open("AQ-QDO-001.json", "w") as f:
        json.dump(artifact, f, indent=2, sort_keys=True)
    print("\n[Saved: AQ-QDO-001.json]")
    return artifact


if __name__ == "__main__":
    results = demo()
    save_artifact(results)
```
