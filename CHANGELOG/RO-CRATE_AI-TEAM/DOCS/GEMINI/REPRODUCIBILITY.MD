# REPRODUCIBILITY.md
# AQARION Research Artifact — Independent Reproduction Checklist

## Execution Protocol
1.  [ ] Clean checkout of the exact Git commit.
2.  [ ] Verify Docker daemon is running for isolated compilation.
3.  [ ] Execute: `pip install -r requirements-strict.txt`
4.  [ ] Execute: `export AQARION_SEED=42`
5.  [ ] Run `python scripts/generate_all.py` (Validates exact Kaprekar rank/defect).
6.  [ ] Run Lean verification: `lake build` (Expect 0 warnings, 0 sorry).
7.  [ ] Run Binding Script: `python scripts/aqarion_binding_protocol.py`.
8.  [ ] Verify PDF embedded hash precisely matches `AQARION_v2.0_FROZEN.zip` SHA-256.
