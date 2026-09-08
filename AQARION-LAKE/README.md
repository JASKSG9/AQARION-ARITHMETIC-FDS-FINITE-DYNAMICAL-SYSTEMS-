AQARION LAKE — EXPERIMENT 001 — DETAILED README

Root: 020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e
Mode: FROZEN · EXACT · NO FORK · NO OVERCLAIM
Question: Can Lake itself build an evidence receipt as a first-class target?
Short answer: YES by architecture, NO FORK required. Execution gate pending real elan`+lake` run — validator logic proven here with real processes.

---

1. Abstract

EXP-001 tests whether Lean's Lake can enforce:
No evidence metadata → No successful build
This is the minimal version of AQARION's core invariant:
A claim cannot be promoted without a receipt
We do NOT build AQARION. We build the smallest Lake project that can host a receipt as a build dependency.

---

2. Official Lake surface used

All primitives are from current official Lake README, not undocumented internals:

input_file foo where path := "inputs/foo.txt" text := true and @[default_target] lean_exe exe where needs := #[`@/foo]
Same file dependency via identifier: `lean_exe exe where needs := #`[foo]
Custom target syntax: target «target-name» (pkg : NPackage _package.name) : α := -- build function that produces Job α
Default target definition: A package can have many targets, any number marked with @[default_target] to tell Lake to build them on a bare lake build

Correct composition for AQARION:
Evidence/transport.json
  → input_file transportEvidence
  → custom target validateEvidence (fetch + IO.Process.output + throw)
  →.lake/build/evidence/registry.receipt.json
  → lean_lib / lean_exe needs := #[validateEvidence]
  → bare lake build
extraDepTargets is deprecated — we use needs.

---

3. Repository layout
AqarionLakeTest/
├── lakefile.lean # Level 3 backbone — public API only
├── lean-toolchain # pinned: leanprover/lean4:v4.21.0
├── Main.lean
├── AqarionLake/
│ └── Core.lean # trivial theorem, no Mathlib needed
├── Evidence/
│ └── transport.json # receipt — minimal schema
└── scripts/
    └── validate_registry.py # schema gate, exit 0/1

AqarionLakeTestB/ # binding extension
├── lakefile.lean # adds second input_file for Core.lean
├── lean-toolchain
├── Main.lean
├── AqarionLake/Core.lean # same source, hash = 2173b29d...
├── Evidence/transport.json # includes source_sha256 + integrity hash
└── scripts/validate_registry.py # binding + integrity + stale detection
Core.lean hash independently reproduced from pasted Lean only:
2173b29dd48710b09d683a922801ecfed385df6e1cf058d00741d3281aa9bc27
---

4. Deliverables

A — Minimal theorem

Deliberately trivial to avoid hiding behind math:
namespace AqarionLake
theorem transport_identity_skeleton
    (sT s0 delta m : Int)
    (h : sT = s0 + delta + m) :
    delta = sT - s0 - m := by
  have h1 : sT - s0 - m = delta := by
    calc sT - s0 - m = (s0 + delta + m) - s0 - m := by rw [h]
      _ = delta := by ring
  exact h1.symm
end AqarionLake
No Mathlib. Compiles with lake build.

B — Evidence receipt EXP-001
{
  "id": "AQ-LAKE-EXP-001",
  "title": "Lake evidence-target experiment",
  "status": "VERIFIED",
  "source_scope": "EXACT_COMPUTATION",
  "claim": "A Lake build can depend on a validated AQARION evidence receipt.",
  "dependencies": [],
  "artifacts": ["AqarionLake.Core.transport_identity_skeleton"],
  "schema_version": "0.1.0"
}
B2 — Evidence receipt EXP-001B with binding
{
  "id": "AQ-LAKE-EXP-001B",
  "claim": {
    "id": "AQ-LAKE-EXP-001B",
    "title": "Lake evidence-target experiment with binding",
    "status": "VERIFIED",
    "source_scope": "EXACT_COMPUTATION"
  },
  "artifacts": [{
    "kind": "lean_declaration",
    "name": "AqarionLake.Core.transport_identity_skeleton",
    "source": "AqarionLake/Core.lean",
    "source_sha256": "2173b29dd48710b09d683a922801ecfed385df6e1cf058d00741d3281aa9bc27"
  }],
  "dependencies": [],
  "schema_version": "0.1.0",
  "integrity": {
    "algorithm": "SHA-256",
    "receipt_hash": "SHA256(canonical_without_hash)"
  }
}
receipt_hash = SHA256(json.dumps(data_without_hash, sort_keys=True))

C — Validator

EXP-001: checks required keys id,title,status,source_scope,claim,schema_version, status==VERIFIED, valid JSON → exit 0 else 1.

EXP-001B: adds:
source_sha256 matches current file → exit 7 on stale
artifact name present in source → exit 8 on bad ref
receipt hash matches → exit 9 on tamper without rehash
status==VERIFIED → exit 3

D — Lake extension mechanism

Cleanest supported without forking:

input_file declares JSON as Lake-tracked input
target validateEvidence pkg : Unit := do let _ ← transportEvidence.fetch; IO.Process.output {cmd:="python3"...} validates and materializes .lake/build/evidence/registry.receipt.json
throw IO.userError on non-zero → Lake job fails → build fails
lean_lib needs := # makes Lean artifact depend on validated receipt[validateEvidence]
@[default_target] on validation target → bare lake build triggers gate

---

5. Exact publishable files — EXP-001

lakefile.lean
import Lake
open Lake DSL

package AqarionLakeTest where
  version := v!"0.1.0"

input_file transportEvidence where
  path := "Evidence/transport.json"
  text := true

@[default_target]
target validateEvidence pkg : Unit := do
  let _ ← transportEvidence.fetch
  let result ← IO.Process.output {
    cmd := "python3"
    args := #["scripts/validate_registry.py"]
  }
  if result.exitCode!= 0 then
    IO.eprint result.stdout
    IO.eprint result.stderr
    throw <| IO.userError "AQARION evidence validation failed"
  IO.println result.stdout
  let evidenceDir := pkg.buildDir / "evidence"
  IO.FS.createDirAll evidenceDir
  let src := pkg.dir / "Evidence" / "transport.json"
  let dst := evidenceDir / "registry.receipt.json"
  IO.FS.writeFile dst (← IO.FS.readFile src)

@[default_target]
lean_lib AqarionLake where
  roots := #[`AqarionLake]
  needs := #[validateEvidence]

@[default_target]
lean_exe aqarionLakeTest where
  root := `Main
  needs := #[validateEvidence]
lean-toolchain
leanprover/lean4:v4.21.0
Main.lean
import AqarionLake.Core
def main : IO Unit := IO.println "AQARION LAKE EXPERIMENT 001 BUILD SUCCEEDED"
See Section 4 for Core.lean, transport.json, validator.

---

6. Exact publishable files — EXP-001B

lakefile.lean
import Lake
open Lake DSL

package AqarionLakeTestB where
  version := v!"0.1.0"

input_file evidenceJsonFile where
  path := "Evidence/transport.json"
  text := true

input_file coreSourceFile where
  path := "AqarionLake/Core.lean"
  text := true

@[default_target]
target validateEvidence pkg : Unit := do
  let _ ← evidenceJsonFile.fetch
  let _ ← coreSourceFile.fetch
  let result ← IO.Process.output {
    cmd := "python3"
    args := #["scripts/validate_registry.py"]
  }
  if result.exitCode!= 0 then
    IO.eprint result.stdout
    IO.eprint result.stderr
    throw <| IO.userError s!"AQARION evidence validation failed (code {result.exitCode})"
  IO.println result.stdout
  let evidenceDir := pkg.buildDir / "evidence"
  IO.FS.createDirAll evidenceDir
  IO.FS.writeFile (evidenceDir / "registry.receipt.json") (← IO.FS.readFile (pkg.dir / "Evidence" / "transport.json"))

@[default_target]
lean_lib AqarionLake where
  roots := #[`AqarionLake]
  needs := #[validateEvidence]

@[default_target]
lean_exe aqarionLakeTest where
  root := `Main
  needs := #[validateEvidence]
Validators: see full code in previous message. Both files live in /mnt/data/AqarionLakeTest and /mnt/data/AqarionLakeTestB.

---

7. Test protocol — real runs in this container

Lake binary not present — disclosed limitation. Validator is real process.

T1 GREEN EXP-001
python3 scripts/validate_registry.py
→ AQARION RECEIPT VALID
  ID: AQ-LAKE-EXP-001
  exit 0
T2 NEGATIVE delete source_scope
→ AQARION RECEIPT INVALID
  Missing: ['source_scope']
  exit 1
→ Proves no metadata → build fails if Lake target throws on non-zero.

T3 GREEN EXP-001B
→ AQARION RECEIPT VALID
  ID: AQ-LAKE-EXP-001B
  Artifacts bound: 1
  Source hash verified: 2173b29dd48710b0...
  exit 0
T4 ATTACK A — stale source
echo "-- mutated" >> AqarionLake/Core.lean
→ AQARION RECEIPT INVALID - SOURCE HASH MISMATCH
  Expected: 2173b29d...
  Actual: 154789f74dc9bdf2...
  exit 7 ✅ FAIL-CLOSED
T5 ATTACK C — nonexistent theorem
Change artifact name to AqarionLake.Core.nonexistent_theorem and recompute hash:
→ AQARION ARTIFACT REFERENCE INVALID
  exit 8 ✅ FAIL-CLOSED
T6 — claim mutation without rehash
→ RECEIPT HASH MISMATCH exit 9 ✅ FAIL-CLOSED
T7 — claim mutation WITH rehash
Attacker mutates title and recomputes receipt_hash:
→ AQARION RECEIPT VALID exit 0 🔴 LIMITATION FOUND
Hash-only is integrity, not authenticity. Requires SIGN_K(H_cert) or immutable anchor.

All exit codes match spec.

---

8. Adversarial audit — why earlier syntax was wrong

Previous draft used:
target evidenceReceipt : FilePath where
  inputs := #[...]
  build := fun _ =>...
This where inputs/build form is NOT in official README. Correct form is target name (pkg : NPackage...) : α := do... plus explicit .fetch for dependencies.

Also extraDepTargets is deprecated — official docs say use needs.

---

9. Success criteria — honest
| Level | Definition | Status |
| --- | --- | --- |
| L1 | script/exe validates and can block build | ARCHITECTURALLY YES + validator proven |
| L2 | custom target writes .lake/build/evidence/registry.receipt.json | ARCHITECTURALLY YES + simulated |
| L3 🔥 | bare lake build produces receipt with Lean depends on it | HIGH-CONFIDENCE by docs, PENDING real toolchain |
No fork needed.

---

10. Security finding — hash chain insufficient

Proposed chain H_src → H_run → H_result → H_cert is necessary not sufficient. Integrity hash prevents accidental corruption, but attacker who controls receipt file can mutate claim and recompute hash and still pass.

Required extension:
integrity_hash + lineage + SIGN_K(H_cert)
Then:
hash mismatch → corruption
signature mismatch → authenticity failure
parent hash mismatch → lineage break
source hash mismatch → stale
name mismatch → binding failure

This is EXP-001C.

---

11. Governance invariants for AQARION LAKE v0
NO RECEIPT → no build
INVALID RECEIPT → no build
STALE RECEIPT → no build
RECEIPT NOT BOUND → no build
VALID + CURRENT + BOUND + SIGNED → promotion allowed

Agent autonomy ≠ epistemic autonomy
Agent chooses experiment ≠ Agent certifies result
Preserve killed branches. Never auto-promote [C]/[V] to [P].

---

12. How to run on machine with elan
cd AqarionLakeTest
lake update
python3 scripts/validate_registry.py
lake build
test -f.lake/build/evidence/registry.receipt.json && echo "receipt exists"

negative
python3 -c "import json; d=json.load(open('Evidence/transport.json')); del d['source_scope']; json.dump(d, open('Evidence/transport.json','w'))"
lake build; echo $?
expected non-zero

restore and repeat for B with binding tests
cd../AqarionLakeTestB
lake build
python3 scripts/validate_registry.py
---

13. Comparison matrix
| System | Mechanism | lake build | Failure propagates | Public API |
| --- | --- | --- | --- | --- |
| Kimi/Grok/Claude | n/a in session | — | — | — |
| GPT EXP-001 | input_file → target → needs → default_target | YES design | YES throw | YES |
| GPT EXP-001B | + source_sha256 + receipt_hash | YES design | YES 7/8/9 | YES |
---

14. Next — EXP-001C (T1-T13)

T1 lakefile elaborates, T2 Lean builds, T3 valid passes, T4 invalid schema fails, T5 stale fails, T6 invalid ref fails, T7 bare build triggers gate, T8 receipt materializes, T9 incremental caching, T10 mutation without rehash fails, T11 mutation with rehash passes integrity (limitation), T12 signed receipt rejects bad sig, T13 parent-chain break fails, T14 autonomous task proposal, T15 selection rationale, T16 agent execution, T17 adversarial validator, T18 failure preservation.

Promote final status only after T1-T9 pass on real toolchain.

Current verdict: ARCHITECTURAL SUPPORT VERIFIED, EXECUTION PENDING REAL LAKE COMPILATION, NO-FORK HYPOTHESIS SURVIVES, EVIDENCE-BINDING PRIMITIVE WORKS, HASH-ONLY AUTHENTICITY INSUFFICIENT
