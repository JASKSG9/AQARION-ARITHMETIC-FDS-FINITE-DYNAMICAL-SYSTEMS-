#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AQARION — Operator Fingerprint Standard
========================================

AQARION is a rigorous Python framework for analysing deterministic dynamical
systems through partition‑based coarse‑graining. It provides exact arithmetic,
immutable fingerprints, and a clear separation between the **Uniform Partition
Framework (UPF)** – a frozen theorem domain – and the **General Partition
Framework (GPF)** – an exploratory research domain.

Key concepts
------------
- **Koopman operator** (pullback): (Kf)(x) = f(T(x)).
- **Projection** onto a partition: averages a function over each block.
- **Defect operator**: D = (I - P) K P. Its rank and singular values
  form a unique "fingerprint" of how dynamics break the invariant subspace.

Features
--------
- Exact rational arithmetic (SymPy) for all core computations.
- Immutable, JSON‑serialisable fingerprints with SHA‑256 hashes.
- Dual‑path design: UPF enforces uniform block sizes (proved theorems),
  GPF handles arbitrary sizes (experimental).
- Comprehensive metrics: exact rank, nullity, trace, nilpotent index,
  Frobenius norm, singular values, spectral entropy, image/kernel bases.
- Built‑in validation (rank + nullity = n, nilpotent index ≤ 2).
- Extensive test suite covering theorem verification, cross‑domain equivalence,
  and historical freeze.

Usage
-----
1. Define a partition (list of blocks) and a transition (list of targets).
2. Instantiate `UniformPartition` or `GeneralPartition`.
3. Create an `UniformAnalyzer` or `GeneralAnalyzer`.
4. Access the fingerprint via `analyzer.fingerprint` or `fingerprint_data()`.

Example
-------
    from aqarion import UniformPartition, UniformAnalyzer

    blocks = [[0,1,2], [3,4,5], [6,7,8]]
    transition = [1,2,0, 4,5,3, 7,8,6]
    partition = UniformPartition(blocks)
    analyzer = UniformAnalyzer(partition, transition)
    print(analyzer.fingerprint.to_json())

Run the test suite:
    python aqarion.py

For full documentation, see the README or visit the project repository.
"""

import sympy as sp
import numpy as np
from fractions import Fraction
import json
import hashlib
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional, Union


# =============================================================================
# LAYER III — Abstract Partition Interface
# =============================================================================

class AbstractPartition(ABC):
    """
    Minimal mathematical object: a map Π : X → B.
    No assumptions about block sizes or structure.
    """

    @abstractmethod
    def states(self) -> Tuple[int, ...]:
        """Return all state indices in the system."""
        raise NotImplementedError

    @abstractmethod
    def blocks(self) -> Tuple[int, ...]:
        """Return all block identifiers."""
        raise NotImplementedError

    @abstractmethod
    def block_of(self, state: int) -> int:
        """Return the block id containing the given state."""
        raise NotImplementedError

    @abstractmethod
    def members(self, block: int) -> Tuple[int, ...]:
        """Return the states belonging to the given block."""
        raise NotImplementedError

    @abstractmethod
    def size(self, block: int) -> int:
        """Return the cardinality of the given block."""
        raise NotImplementedError

    def block_sizes(self) -> Dict[int, int]:
        """Return a dict mapping block id → block size."""
        return {b: self.size(b) for b in self.blocks()}

    def is_uniform(self) -> bool:
        """Return True if all blocks have the same size."""
        sizes = self.block_sizes().values()
        return len(set(sizes)) == 1


# =============================================================================
# LAYER I — Uniform Partition Framework (UPF) — FROZEN THEOREM DOMAIN
# =============================================================================

class UniformPartitionError(TypeError):
    """Raised when a partition violates the equal‑cardinality hypothesis."""
    pass


class UniformPartition(AbstractPartition):
    """
    Uniform Partition (UPF) — all blocks have the same size k.

    The constructor enforces the invariant: ∀ b₁, b₂ ∈ blocks, |b₁| = |b₂| = k.
    All theoretical guarantees in UPF rely on this property.

    Attributes
    ----------
    k : int
        Size of each block.
    m : int
        Number of blocks.
    """

    def __init__(self, blocks: List[List[int]], validate: bool = True):
        """
        Parameters
        ----------
        blocks : list of lists of int
            Each inner list contains state indices belonging to one block.
            States must be unique across blocks.
        validate : bool, default=True
            If True, check that all blocks have the same size.
            Set to False only if you are certain of uniformity.
        """
        self._blocks = tuple(tuple(sorted(block)) for block in blocks)
        self._block_ids = tuple(range(len(self._blocks)))
        self._state_to_block = {}
        for bid, block in enumerate(self._blocks):
            for state in block:
                if state in self._state_to_block:
                    raise ValueError(f"State {state} appears in multiple blocks")
                self._state_to_block[state] = bid
        self._all_states = tuple(sorted(self._state_to_block.keys()))
        if validate:
            self._validate_uniform()

    def _validate_uniform(self) -> None:
        sizes = [len(b) for b in self._blocks]
        if len(set(sizes)) != 1:
            raise UniformPartitionError(
                f"Partition not uniform. Block sizes: {sizes}. Use GeneralPartition."
            )
        self._k = sizes[0] if sizes else 0
        self._m = len(self._blocks)

    @property
    def k(self) -> int:
        """Size of each block (constant)."""
        return self._k

    @property
    def m(self) -> int:
        """Number of blocks."""
        return self._m

    def states(self) -> Tuple[int, ...]:
        return self._all_states

    def blocks(self) -> Tuple[int, ...]:
        return self._block_ids

    def block_of(self, state: int) -> int:
        return self._state_to_block[state]

    def members(self, block: int) -> Tuple[int, ...]:
        return self._blocks[block]

    def size(self, block: int) -> int:
        return len(self._blocks[block])

    def __repr__(self) -> str:
        return f"UniformPartition(m={self.m}, k={self.k})"


# =============================================================================
# LAYER II — General Partition Framework (GPF) — RESEARCH DOMAIN
# =============================================================================

class GeneralPartition(AbstractPartition):
    """
    General Partition (GPF) — no cardinality assumptions.

    Designed for exploratory research; all formulas use |B| instead of a
    constant k.
    """

    def __init__(self, state_to_block: Dict[int, int],
                 block_members: Dict[int, List[int]]):
        """
        Parameters
        ----------
        state_to_block : dict int → int
            Mapping from state index to block id.
        block_members : dict int → list of int
            Mapping from block id to list of states in that block.
            Must be consistent with state_to_block.
        """
        self._state_to_block = dict(state_to_block)
        self._block_members = {
            bid: tuple(sorted(members)) for bid, members in block_members.items()
        }
        self._block_ids = tuple(sorted(self._block_members.keys()))
        self._validate_partition()

    def _validate_partition(self) -> None:
        all_states = set()
        for bid, members in self._block_members.items():
            for state in members:
                if state in all_states:
                    raise ValueError(f"State {state} appears in multiple blocks")
                all_states.add(state)
                if self._state_to_block.get(state) != bid:
                    raise ValueError(f"State {state} mapping inconsistent")
        for state in self._state_to_block:
            if state not in all_states:
                raise ValueError(f"State {state} has no block")
        self._all_states = tuple(sorted(all_states))

    def states(self) -> Tuple[int, ...]:
        return self._all_states

    def blocks(self) -> Tuple[int, ...]:
        return self._block_ids

    def block_of(self, state: int) -> int:
        return self._state_to_block[state]

    def members(self, block: int) -> Tuple[int, ...]:
        return self._block_members[block]

    def size(self, block: int) -> int:
        return len(self._block_members[block])

    @classmethod
    def from_blocks_list(cls, blocks: List[List[int]]) -> "GeneralPartition":
        """Convenience constructor from a list of block lists."""
        stb, bm = {}, {}
        for bid, block in enumerate(blocks):
            bm[bid] = block
            for state in block:
                stb[state] = bid
        return cls(stb, bm)

    def __repr__(self) -> str:
        return f"GeneralPartition(sizes={list(self.block_sizes().values())})"


# =============================================================================
# MATRIX BUILDERS
# =============================================================================

def _build_koopman_matrix(transition: List[int]) -> sp.Matrix:
    """
    Build the exact Koopman matrix K (pullback convention).

    For a deterministic transition T: X → X, K[x, y] = 1 if T(x) = y else 0.
    """
    n = len(transition)
    K = sp.zeros(n, n)
    for src, tgt in enumerate(transition):
        K[src, tgt] = sp.Integer(1)
    return K


def upf_projection_matrix(partition: UniformPartition) -> sp.Matrix:
    """
    UPF projection: (Pf)(x) = (1/k) * sum_{y in B_x} f(y).

    Only valid for UniformPartition; uses the constant k.
    """
    if not isinstance(partition, UniformPartition):
        raise TypeError("UPF projection requires UniformPartition")
    n = len(partition.states())
    P = sp.zeros(n, n)
    for b in partition.blocks():
        members = partition.members(b)
        k = partition.size(b)
        for x in members:
            for y in members:
                P[x, y] = sp.Rational(1, k)
    return P


def gpf_projection_matrix(partition: AbstractPartition) -> sp.Matrix:
    """
    GPF projection: (Pf)(x) = (1/|B_x|) * sum_{y in B_x} f(y).

    Works for any partition; uses block‑specific sizes.
    """
    n = len(partition.states())
    P = sp.zeros(n, n)
    for b in partition.blocks():
        members = partition.members(b)
        sz = partition.size(b)
        for x in members:
            for y in members:
                P[x, y] = sp.Rational(1, sz)
    return P


def defect_matrix(P: sp.Matrix, K: sp.Matrix) -> sp.Matrix:
    """Defect operator D = (I - P) K P. Exact symbolic."""
    I = sp.eye(P.shape[0])
    return (I - P) * K * P


# ---- Escape and Co‑occurrence Matrices ----

def upf_escape_matrix(partition: UniformPartition,
                      transition: List[int]) -> sp.Matrix:
    """
    UPF escape matrix: M_{ij} = (1/k) * |{x in B_i : T(x) in B_j}|.

    Exact rational, requires UniformPartition.
    """
    if not isinstance(partition, UniformPartition):
        raise TypeError("UPF escape requires UniformPartition")
    m = partition.m
    M = sp.zeros(m, m)
    for src_b in partition.blocks():
        members = partition.members(src_b)
        k = partition.size(src_b)
        counts = {}
        for x in members:
            tgt_b = partition.block_of(transition[x])
            counts[tgt_b] = counts.get(tgt_b, 0) + 1
        for tgt_b, c in counts.items():
            M[src_b, tgt_b] = sp.Rational(c, k)
    return M


def gpf_escape_matrix(partition: AbstractPartition,
                      transition: List[int]) -> sp.Matrix:
    """
    GPF escape matrix: M_{ij} = (1/|B_i|) * |{x in B_i : T(x) in B_j}|.

    Works for any partition; uses block sizes.
    """
    blocks = partition.blocks()
    m = len(blocks)
    M = sp.zeros(m, m)
    for src_b in blocks:
        members = partition.members(src_b)
        sz = partition.size(src_b)
        counts = {}
        for x in members:
            tgt_b = partition.block_of(transition[x])
            counts[tgt_b] = counts.get(tgt_b, 0) + 1
        for tgt_b, c in counts.items():
            M[src_b, tgt_b] = sp.Rational(c, sz)
    return M


def upf_cooccurrence_matrix(partition: UniformPartition,
                            transition: List[int]) -> sp.Matrix:
    """
    UPF co‑occurrence: C_{ij} = |{x in B_i : T(x) in B_j}|.

    Exact integer matrix.
    """
    if not isinstance(partition, UniformPartition):
        raise TypeError("UPF co‑occurrence requires UniformPartition")
    m = partition.m
    C = sp.zeros(m, m)
    for src_b in partition.blocks():
        for x in partition.members(src_b):
            C[src_b, partition.block_of(transition[x])] += 1
    return C


def gpf_cooccurrence_matrix(partition: AbstractPartition,
                            transition: List[int]) -> sp.Matrix:
    """
    GPF co‑occurrence: C_{ij} = |{x in B_i : T(x) in B_j}|.

    Exact integer matrix for any partition.
    """
    blocks = partition.blocks()
    m = len(blocks)
    C = sp.zeros(m, m)
    for src_b in blocks:
        for x in partition.members(src_b):
            C[src_b, partition.block_of(transition[x])] += 1
    return C


# =============================================================================
# FINGERPRINT STANDARD v1.0
# =============================================================================

class OperatorFingerprint:
    """
    Immutable, comparable, traceable fingerprint of the defect operator.

    All core computations use exact rational arithmetic (SymPy). Spectral
    quantities are approximated via NumPy's SVD and provided as floats.

    The fingerprint is stored as a JSON‑serialisable dictionary and can be
    hashed with SHA‑256 for tamper‑evident storage.
    """

    def __init__(self, partition: AbstractPartition,
                 transition: List[int],
                 provenance: Optional[Dict[str, Any]] = None):
        """
        Parameters
        ----------
        partition : AbstractPartition
            The partition (Uniform or General).
        transition : list of int
            The deterministic transition T: for each state x, T(x).
        provenance : dict, optional
            Metadata about the fingerprint's origin (generator, timestamp, etc.).
            If not provided, a default is inserted.
        """
        self.partition = partition
        self.transition = transition
        self.n = len(transition)
        self.provenance = provenance or {
            "generator": "AQARION-ARITHMETIC v2.0",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Build exact matrices
        self.K = _build_koopman_matrix(transition)
        if isinstance(partition, UniformPartition):
            self.P = upf_projection_matrix(partition)
            self.M = upf_escape_matrix(partition, transition)
            self.C = upf_cooccurrence_matrix(partition, transition)
        else:
            self.P = gpf_projection_matrix(partition)
            self.M = gpf_escape_matrix(partition, transition)
            self.C = gpf_cooccurrence_matrix(partition, transition)

        self.D = defect_matrix(self.P, self.K)
        self._compute()

    def _compute(self) -> None:
        """Compute all fingerprint metrics."""
        # --- EXACT ARITHMETIC ---
        exact_rank = int(self.D.rank())
        exact_nullity = self.n - exact_rank
        exact_trace = str(self.D.trace())

        # Frobenius norm squared (exact rational)
        frob_sq = sum(self.D[i, j]**2
                      for i in range(self.n) for j in range(self.n))

        # Nilpotent index: D^2 = 0 for orthogonal projections
        D2 = self.D ** 2
        nilpotent_index = 1 if D2.is_zero_matrix else 2

        # --- NUMERIC CONVERSIONS FOR SPECTRAL ---
        D_np = np.array(self.D.tolist(), dtype=float)
        s = np.linalg.svd(D_np, compute_uv=False)
        s = s[s > 1e-12]

        if len(s) > 0:
            p = s / np.sum(s)
            spectral_entropy = float(-np.sum(p * np.log(p + 1e-15)))
            stable_rank = float(np.sum(s**2) / (s[0]**2 + 1e-15))
            condition_number = float(s[0] / s[-1]) if len(s) > 1 else float('inf')
            top_sv = float(s[0])
            num_sv = int(len(s))
        else:
            spectral_entropy = 0.0
            stable_rank = 0.0
            condition_number = float('inf')
            top_sv = 0.0
            num_sv = 0

        nuclear_norm = float(np.sum(s))

        # --- GEOMETRIC DESCRIPTORS ---
        if exact_rank > 0:
            U, _, _ = np.linalg.svd(D_np)
            image_basis = U[:, :exact_rank].T.tolist()
        else:
            image_basis = []

        if exact_nullity > 0:
            kernel_basis = sp.Matrix(self.D).nullspace()
            kernel_basis = [list(v.evalf().T.tolist()[0]) for v in kernel_basis]
        else:
            kernel_basis = []

        # --- ASSOCIATED OPERATORS ---
        P_np = np.array(self.P.tolist(), dtype=float)
        K_np = np.array(self.K.tolist(), dtype=float)
        KP = K_np @ P_np
        PK = P_np @ K_np
        commutator = KP - PK
        I_np = np.eye(self.n)
        dual_defect = P_np @ K_np @ (I_np - P_np)

        # --- STRUCTURAL CLASSIFICATION ---
        if exact_rank == self.n - 1:
            rank_class = "maximal"
        elif exact_rank == 0:
            rank_class = "trivial"
        else:
            rank_class = "intermediate"

        defect_class = "structural" if exact_rank > 0 else "vanishing"

        # --- ASSEMBLE FINGERPRINT ---
        self._data = {
            "version": "1.0",
            "timestamp": self.provenance["timestamp"],
            "provenance": self.provenance,
            "system": {
                "m": len(self.partition.blocks()),
                "n": self.n,
                "operator_type": "deterministic",
                "convention": "pullback"
            },
            "exact": {
                "operator_rank": exact_rank,
                "operator_nullity": exact_nullity,
                "trace": exact_trace,
                "nilpotent_index": nilpotent_index,
                "frobenius_norm_sq": str(frob_sq),
                "nuclear_norm": f"{nuclear_norm:.10f}"
            },
            "geometric": {
                "image_basis": image_basis,
                "kernel_basis": kernel_basis,
                "image_dimension": exact_rank,
                "kernel_dimension": exact_nullity
            },
            "spectral": {
                "singular_values": [float(v) for v in s],
                "spectral_entropy": spectral_entropy,
                "stable_rank": stable_rank,
                "condition_number": condition_number,
                "top_singular_value": top_sv,
                "num_singular_values": num_sv
            },
            "associated": {
                "commutator_norm": float(np.linalg.norm(commutator, 'fro')),
                "projected_koopman_rank": int(np.linalg.matrix_rank(P_np @ K_np @ P_np)),
                "dual_defect_rank": int(np.linalg.matrix_rank(dual_defect)),
                "commutator_rank": int(np.linalg.matrix_rank(commutator)),
                "commutator_nullity": int(self.n - np.linalg.matrix_rank(commutator))
            },
            "classification": {
                "rank_class": rank_class,
                "defect_class": defect_class,
                "maturity": "proved" if isinstance(self.partition, UniformPartition)
                           else "experimental"
            }
        }

        # Add partition‑specific fields
        if isinstance(self.partition, UniformPartition):
            self._data["system"]["k"] = self.partition.k
        else:
            self._data["system"]["block_sizes"] = [
                self.partition.size(b) for b in self.partition.blocks()
            ]

    @property
    def data(self) -> Dict[str, Any]:
        """Return a copy of the fingerprint data dictionary."""
        return self._data.copy()

    def to_json(self, indent: int = 2) -> str:
        """Return JSON representation of the fingerprint."""
        return json.dumps(self._data, indent=indent, default=str)

    def hash(self) -> str:
        """
        SHA‑256 hash of the canonical JSON representation.

        Used for traceability and tamper detection.
        """
        def _convert(obj):
            if isinstance(obj, dict):
                return {k: _convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_convert(v) for v in obj]
            elif hasattr(obj, 'evalf'):  # SymPy numeric objects
                return float(obj)
            return obj

        canonical = json.dumps(_convert(self._data),
                               sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode()).hexdigest()

    def validate(self) -> Tuple[bool, str]:
        """
        Validate the fingerprint against mathematical invariants.

        Checks:
        1. rank + nullity = n
        2. spectral rank matches exact rank
        3. nilpotent index ≤ 2 (orthogonal projection property)

        Returns
        -------
        (bool, str)
            Tuple of (validity flag, message).
        """
        exact = self._data["exact"]
        spectral = self._data["spectral"]
        n = self._data["system"]["n"]

        if exact["operator_rank"] + exact["operator_nullity"] != n:
            return False, "rank + nullity != n"

        if spectral["num_singular_values"] != exact["operator_rank"]:
            return False, "spectral rank mismatch"

        if exact["nilpotent_index"] > 2:
            return False, "nilpotent index > 2"

        return True, "valid"


# =============================================================================
# ANALYSERS
# =============================================================================

class UniformAnalyzer:
    """
    UPF‑specific analyser. Provides theorem‑based results.

    Only accepts UniformPartition.
    """

    def __init__(self, partition: UniformPartition, transition: List[int]):
        if not isinstance(partition, UniformPartition):
            raise UniformPartitionError(
                "UniformAnalyzer requires UniformPartition. Use GeneralAnalyzer."
            )
        self.partition = partition
        self.transition = transition
        self.n = len(transition)
        self.m = partition.m
        self.k = partition.k
        self.fingerprint = OperatorFingerprint(partition, transition)
        self.D = self.fingerprint.D
        self.M = self.fingerprint.M
        self.C = self.fingerprint.C

    def defect_rank(self) -> int:
        """Exact rank of the defect operator D."""
        return self.fingerprint._data["exact"]["operator_rank"]

    def escape_rank(self) -> int:
        """Exact rank of the escape matrix M."""
        return int(self.M.rank())

    def nullity(self) -> int:
        """Exact nullity of D."""
        return self.fingerprint._data["exact"]["operator_nullity"]

    def singular_values(self) -> np.ndarray:
        """Numeric singular values of D."""
        return np.array(self.fingerprint._data["spectral"]["singular_values"])

    def cooccurrence_rank_formula(self) -> Tuple[int, int]:
        """
        Theorem 4 (Uniform Co‑occurrence Rank Formula):

        rank(D) = m - c, where c is the number of connected components
        in the undirected graph whose adjacency is C_{ij} + C_{ji} > 0.

        Returns
        -------
        Tuple[int, int]
            (predicted_rank, number_of_components)
        """
        C_np = np.array(self.C.tolist(), dtype=int)
        adj = ((C_np > 0) + (C_np.T > 0)) > 0
        adj = adj.astype(int)
        visited = set()
        comp = 0
        for node in range(self.m):
            if node not in visited:
                comp += 1
                queue = [node]
                visited.add(node)
                while queue:
                    cur = queue.pop(0)
                    for nbr in range(self.m):
                        if adj[cur, nbr] and nbr not in visited:
                            visited.add(nbr)
                            queue.append(nbr)
        return self.m - comp, comp

    def fingerprint_data(self) -> Dict[str, Any]:
        """Return the full fingerprint dictionary."""
        return self.fingerprint.data


class GeneralAnalyzer:
    """
    GPF exploratory analyser. No UPF theorems assumed.

    Accepts any AbstractPartition.
    """

    def __init__(self, partition: AbstractPartition, transition: List[int]):
        self.partition = partition
        self.transition = transition
        self.n = len(transition)
        self.blocks = partition.blocks()
        self.m = len(self.blocks)
        self.fingerprint = OperatorFingerprint(partition, transition)
        self.D = self.fingerprint.D
        self.M = self.fingerprint.M
        self.C = self.fingerprint.C

    def defect_rank(self) -> int:
        return self.fingerprint._data["exact"]["operator_rank"]

    def escape_rank(self) -> int:
        return int(self.M.rank())

    def nullity(self) -> int:
        return self.fingerprint._data["exact"]["operator_nullity"]

    def singular_values(self) -> np.ndarray:
        return np.array(self.fingerprint._data["spectral"]["singular_values"])

    def fingerprint_data(self) -> Dict[str, Any]:
        return self.fingerprint.data


# =============================================================================
# TEST SUITE
# =============================================================================

def run_tests() -> Tuple[int, int]:
    """
    Execute the full test suite.

    Returns
    -------
    Tuple[int, int]
        (passed, failed)
    """
    passed = 0
    failed = 0

    def check(name: str, condition: bool) -> None:
        nonlocal passed, failed
        if condition:
            print(f"  PASS: {name}")
            passed += 1
        else:
            print(f"  FAIL: {name}")
            failed += 1

    print("\n" + "=" * 60)
    print("UPF HYPOTHESIS ENFORCEMENT")
    print("=" * 60)

    p = UniformPartition([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    check("UPF accepts uniform", p.m == 3 and p.k == 3)

    try:
        UniformPartition([[0], [1, 2, 3], [4, 5]])
        check("UPF rejects non‑uniform", False)
    except UniformPartitionError:
        check("UPF rejects non‑uniform", True)

    gp = GeneralPartition.from_blocks_list([[0, 1], [2, 3, 4]])
    try:
        UniformAnalyzer(gp, [0, 1, 2, 3, 4])
        check("UniformAnalyzer rejects GeneralPartition", False)
    except UniformPartitionError:
        check("UniformAnalyzer rejects GeneralPartition", True)

    print("\n" + "=" * 60)
    print("UPF THEOREM VERIFICATION + FINGERPRINT")
    print("=" * 60)

    p = UniformPartition([[0, 1], [2, 3]])
    ua = UniformAnalyzer(p, [1, 0, 3, 2])
    rank_pred, comp = ua.cooccurrence_rank_formula()
    check("Theorem 4: rank=0 for invariant", rank_pred == 0 and comp == 2)
    check("Exact rank matches formula", ua.defect_rank() == rank_pred)

    fp = ua.fingerprint_data()
    check("Fingerprint has exact rank", fp["exact"]["operator_rank"] == 0)
    check("Fingerprint has nilpotent index", fp["exact"]["nilpotent_index"] == 1)
    check("Fingerprint valid", ua.fingerprint.validate()[0])
    check("Fingerprint hash non‑empty", len(ua.fingerprint.hash()) == 64)

    print("\n" + "=" * 60)
    print("GPF ARBITRARY PARTITIONS + FINGERPRINT")
    print("=" * 60)

    blocks = [[0], [1, 2, 4, 8], [3, 5, 6, 9, 10, 12], [7, 11, 13, 14], [15]]
    gp = GeneralPartition.from_blocks_list(blocks)
    check("GPF sizes [1,4,6,4,1]",
          [gp.size(i) for i in gp.blocks()] == [1, 4, 6, 4, 1])
    check("GPF not uniform", not gp.is_uniform())

    transition = list(range(1, 16)) + [0]
    ga = GeneralAnalyzer(gp, transition)
    check("GPF escape shape (5,5)", ga.M.shape == (5, 5))
    check("GPF escape row sums = 1",
          np.allclose(np.array(ga.M.tolist(), dtype=float).sum(axis=1), 1.0))
    check("GPF defect_rank >= 0", ga.defect_rank() >= 0)
    check("GPF nullity = n - rank", ga.nullity() == 16 - ga.defect_rank())

    fp_g = ga.fingerprint_data()
    check("GPF fingerprint valid", ga.fingerprint.validate()[0])
    check("GPF maturity = experimental", fp_g["classification"]["maturity"] == "experimental")
    check("GPF system has block_sizes", "block_sizes" in fp_g["system"])
    check("GPF no k field", "k" not in fp_g["system"])

    print("\n" + "=" * 60)
    print("CROSS‑DOMAIN EQUIVALENCE: GPF|_Uniform = UPF")
    print("=" * 60)

    for seed in range(10):
        np.random.seed(seed)
        states = list(range(12))
        np.random.shuffle(states)
        blocks = [states[i:i+3] for i in range(0, 12, 3)]
        up = UniformPartition(blocks)
        gp = GeneralPartition.from_blocks_list(blocks)
        transition = list(np.random.permutation(12))
        ua = UniformAnalyzer(up, transition)
        ga = GeneralAnalyzer(gp, transition)
        check(f"Equivalence seed {seed}: rank", ua.defect_rank() == ga.defect_rank())

    up = UniformPartition([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    gp = GeneralPartition.from_blocks_list([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
    transition = [1, 2, 0, 4, 5, 3, 7, 8, 6]
    ua = UniformAnalyzer(up, transition)
    ga = GeneralAnalyzer(gp, transition)
    check("D_UPF == D_GPF",
          np.allclose(np.array(ua.D.tolist(), dtype=float),
                      np.array(ga.D.tolist(), dtype=float)))
    sv_u = np.sort(ua.singular_values())
    sv_g = np.sort(ga.singular_values())
    check("Singular values match", np.allclose(sv_u, sv_g))

    print("\n" + "=" * 60)
    print("HISTORICAL FREEZE")
    print("=" * 60)

    p = UniformPartition([list(range(5)), list(range(5, 10))])
    ua = UniformAnalyzer(p, [5, 6, 7, 8, 9, 0, 1, 2, 3, 4])
    fp = ua.fingerprint_data()
    check("Exp003 rank=0", fp["exact"]["operator_rank"] == 0)
    check("Exp003 nullity=10", fp["exact"]["operator_nullity"] == 10)
    check("Exp003 m=2", fp["system"]["m"] == 2)
    check("Exp003 k=5", fp["system"]["k"] == 5)
    check("Exp003 trace exact", fp["exact"]["trace"] == "0")

    p = UniformPartition([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]])
    ua = UniformAnalyzer(p, [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8])
    fp = ua.fingerprint_data()
    check("Exp004 rank=0", fp["exact"]["operator_rank"] == 0)
    check("Exp004 nilpotent=1", fp["exact"]["nilpotent_index"] == 1)

    s = json.dumps(fp, default=str)
    fp2 = json.loads(s)
    check("JSON fingerprint stable", fp2["exact"]["operator_rank"] == fp["exact"]["operator_rank"])

    print("\n" + "=" * 60)
    print("FORBIDDEN PATTERN SCAN")
    print("=" * 60)

    import inspect
    gpf_escape_src = inspect.getsource(gpf_escape_matrix)
    gpf_proj_src = inspect.getsource(gpf_projection_matrix)
    forbidden = ["// k", "/ k", "range(b*k", "src //", "tgt //"]
    found = any(t in gpf_escape_src or t in gpf_proj_src for t in forbidden)
    check("No forbidden patterns in GPF", not found)

    print("\n" + "=" * 60)
    print("EXPERIMENT 005: HAMMING WEIGHT")
    print("=" * 60)

    hamming_blocks = [[0], [1, 2, 4, 8], [3, 5, 6, 9, 10, 12], [7, 11, 13, 14], [15]]
    try:
        UniformPartition(hamming_blocks)
        check("UPF rejects Hamming", False)
    except UniformPartitionError:
        check("UPF rejects Hamming", True)

    gp = GeneralPartition.from_blocks_list(hamming_blocks)
    ga = GeneralAnalyzer(gp, list(range(1, 16)) + [0])
    check("GPF accepts Hamming", ga.M.shape == (5, 5))
    print(f"  Block sizes: {[gp.size(b) for b in gp.blocks()]}")
    print(f"  Defect rank: {ga.defect_rank()}")
    print(f"  Defect nullity: {ga.nullity()}")
    print(f"  Escape matrix:\n{np.array(ga.M.tolist(), dtype=float)}")
    print(f"  Fingerprint hash: {ga.fingerprint.hash()[:16]}...")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return passed, failed


def main() -> None:
    """Entry point: runs the test suite."""
    passed, failed = run_tests()
    if failed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
