/**
 * AQARION RAG-LUT.ts
 * Frozen Retrieval-Augmented Generation Lookup Table
 * Root: 020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e
 * Mode: FROZEN · EXACT · NO FABRICATION · NO PROMOTION
 * Lean: OPEN · C4: BLOCKED · Publication: BLOCKED
 *
 * Purpose: Single source of truth for entire session progress.
 * r ≠ ρ_T must never be conflated.
 */

// ------------------------------------------------------------------
// Types
// ------------------------------------------------------------------

export type ClaimStatus =
  | "PROVED"
  | "CONFIRMED"
  | "VERIFIED"
  | "REJECTED"
  | "REFUTED"
  | "OPEN"
  | "BLOCKED"
  | "CONJECTURE"
  | "V-sample";

export interface ClaimEntry {
  id: string;
  statement: string;
  status: ClaimStatus;
  evidence: string;
  scope?: string;
}

export interface FrozenDefinitions {
  r: string;
  s: string;
  rho_T: string;
  J_T: string;
  m: string;
  DeltaPlus: string;
  S: string;
}

// ------------------------------------------------------------------
// Frozen definitions — DO NOT CHANGE without re-audit
// ------------------------------------------------------------------

export const FROZEN_DEFINITIONS: FrozenDefinitions = {
  r: "r(Pi) = n - |Pi| — ordinary partition-lattice rank",
  s: "s(Pi,Sigma) = r(Pi)+r(Sigma)-r(Pi meet Sigma)-r(Pi join Sigma) — ordinary slack, >=0 by semimodularity",
  rho_T: "rho_T(Pi) = rank((I-P_Pi) K_T P_Pi) = |Pi| - c(H_{Pi,T}) — AQARION defect rank, NOT globally submodular",
  J_T: "J_T(Pi) = Pi join T(Pi) — dynamical join, join-preserving for permutations",
  m: "m = r(J_T Pi meet J_T Sigma) - r(J_T(Pi meet Sigma)) — meet defect, >=0 for perms",
  DeltaPlus: "Delta^+ = rho(join)-rho(Pi)-rho(Sigma)+rho(meet) — violation iff >0",
  S: "S = Delta^+ - s_0 = -s_image - m — residual, <=0 for perms (theorem)",
};

export const SIGN_CONVENTION =
  "Delta^+ = s0 - s_image - m, with s0=s(Pi,Sigma), s_image=s(J_T Pi,J_T Sigma), m>=0. Plus-sign version Delta^+=s0-s_image+m is REFUTED.";

// ------------------------------------------------------------------
// Transport identity (corrected)
// ------------------------------------------------------------------

export const TRANSPORT_IDENTITY = {
  id: "AQ-TRANSPORT-ID-001",
  formula: "Delta^+_T(Pi,Sigma) = s0 - s_image - m_T(Pi,Sigma)",
  status: "PROVED" as ClaimStatus,
  proof_sketch: [
    "rho_T(Pi)=r(J_T Pi)-r(Pi) for bijections (H-components <-> J-blocks)",
    "J_T(Pi join Sigma)=J_T Pi join J_T Sigma (T is lattice automorphism)",
    "Expand Delta^+ via r(J_T·)-r(·), collect terms",
    "Meet defect m accounts for J_T not preserving meets",
  ],
  refuted_variant: "Delta^+=s0-s_image+m — REFUTED (2184/5400 failures at n=4)",
};

// ------------------------------------------------------------------
// S6 exhaustive census (V144 reinstated)
// ------------------------------------------------------------------

export const S6_CENSUS = {
  n: 6,
  permutations: 720,
  partitions: 203, // B6
  pairs_per_perm: 20706, // 203*204/2 including Pi=Sigma
  total_tests: 14908320,
  violations: 5760,
  perms_violating: 430,
  delta_range: [-4, 1] as [number, number],
  violation_signature: "(s0,s_image,m)=(1,0,0) — 5760/5760",
  unit_slack_pairs_per_perm: 2955,
  total_unit_slack: 2127600,
  matrix_crosscheck: "6/6 PASS (support-graph rho = exact rational rank)",
  cycle_table: [
    { type: "1^6", perms: 1, violating: 0 },
    { type: "2+1^4", perms: 15, violating: 0 },
    { type: "2+2+1+1", perms: 45, violating: 45 },
    { type: "2+2+2", perms: 15, violating: 15 },
    { type: "3+1^3", perms: 40, violating: 0 },
    { type: "3+2+1", perms: 120, violating: 120 },
    { type: "3+3", perms: 40, violating: 40 },
    { type: "4+1^2", perms: 90, violating: 0 },
    { type: "4+2", perms: 90, violating: 90 },
    { type: "5+1", perms: 144, violating: 0 },
    { type: "6", perms: 120, violating: 120 },
  ],
};

// ------------------------------------------------------------------
// S7 spot checks
// ------------------------------------------------------------------

export const S7_SPOT = {
  total_perms: 5040,
  note: "Full 1.94B census NOT rerun; spot-checks only",
  seven_cycles: { k1_violations: 427, k2_violations: 427, delta_range: [-6, 1] as [number, number] },
  boundary: [
    { type: "2+1^5", perms: 21, violations: 0 },
    { type: "3+1^4", perms: 70, violations: 0 },
    { type: "4+1^3", perms: 210, violations: 72 },
    { type: "5+1^2", perms: 504, violations: 240 },
    { type: "6+1", perms: 840, violations: 390 },
  ],
};

// ------------------------------------------------------------------
// Anchor thresholds — [V-sample] only, predicate must be frozen
// ------------------------------------------------------------------

export const ANCHOR_THRESHOLDS = {
  predicate: "f^*_{exists,U}(k) = min{f>=0: exists T in S_{k+f} type (k,1^f), exists (Pi,Sigma) in U_{k+f} with s0=1 and Delta^+=1}",
  warning: "U_n must be frozen (e.g. crossing-doubleton pairs). Do not infer f^*(k)=8-k; 8-6=2 !=0.",
  observed: [
    { k: 6, f_star: 0, note: "self-anchoring" },
    { k: 5, f_star: 2, note: "needs 2 fixed points" },
    { k: 4, f_star: 3, note: "needs 3 fixed points" },
  ],
  n8_targeted_test: {
    "3+1^5": { pairs_tested: 210, violations: 0, status: "V-sample" as ClaimStatus },
    "2+1^6": { pairs_tested: 210, violations: 0, status: "V-sample" as ClaimStatus },
  },
};

// ------------------------------------------------------------------
// Master ledger — honest adversarial audit
// ------------------------------------------------------------------

export const LEDGER: ClaimEntry[] = [
  { id: "AQ-TRANSPORT-ID-001", statement: "Delta^+=s0-s_image-m", status: "PROVED", evidence: "0 failures / 14.9M pairs; sign corrected" },
  { id: "AQ-S-LE-ZERO", statement: "S=-s_image-m <=0 for perms", status: "PROVED", evidence: "s_image>=0 (ordinary lattice), m>=0 (order)" },
  { id: "AQ-TRIVIAL-SLACK", statement: "s(1,Sigma)=0", status: "PROVED", evidence: "1 join Sigma=1, 1 meet Sigma=Sigma" },
  { id: "AQ-TRIVIAL-SUFF", statement: "s0=1 & J_T Pi=1 & m=0 => Delta^+=1", status: "PROVED", evidence: "Via transport identity" },
  { id: "AQ-TRIVIAL-NECESSITY", statement: "Trivialization necessary", status: "REFUTED", evidence: "
