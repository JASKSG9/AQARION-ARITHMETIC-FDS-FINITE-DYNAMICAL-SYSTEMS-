# PROVENANCE.md
# AQARION Research Artifact — Provenance Metadata
# Directive: AQ-2026-011

## Environment
- OS: Linux (Ubuntu 22.04 LTS / Docker frozen)
- Architecture: x86_64
- Deterministic Timestamp (`SOURCE_DATE_EPOCH`): 1704067200

## Formal Verification Toolchain (Strict Pinning)
- Compiler: Lean 4 (`v4.7.0`)
- Mathlib4 Commit: `d8a264a787...` (Pinned in `lean-toolchain` and `lake-manifest.json`)
- Verification Target: `FinDet.Core` and `FinDet.Quotient` (0 sorry)

## Canonical Serialization & Hardware Translation
- Floating-Point: Strictly integer/rational exact arithmetic for Level I/II fingerprints.
- Substrate Target: Type II-k[$\epsilon$] calculations modeled against generic continuous-time analog memristor crossbars.
