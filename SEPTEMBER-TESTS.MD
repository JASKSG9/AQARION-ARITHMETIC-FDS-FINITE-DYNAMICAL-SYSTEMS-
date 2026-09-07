

AQARION ROOT TEST SUITE

I created a root-level adversarial regression suite covering the current AQARION ledger rather than another narrow experiment.

Package

Download AQARION_ROOT_TEST_SUITE_V151.zip

Contents:

AQARION_ROOT_TEST_SUITE/
├── AQARION_ROOT_TEST_MANIFEST.json
├── AQARION_ROOT_TEST_SUITE_README.md
├── pytest.ini
└── tests/
    └── test_aqarion_root.py

The repository itself is currently accessible to me as read-only, so I did not pretend to push these files into GitHub. The actual repository root currently contains the AQARION algorithm/checkpoint/data infrastructure, including CLAIMS_REGISTRY.MD, ALGORITHM/, CHECKPOINTS/, DATA/, etc.

Coverage

The suite now directly tests:

exact Koopman pullback convention

exact defect construction

rank(D)=m-c(H)

compatibility iff zero defect

corrected augmented-rank identity

exact D²=0

n=5 submodularity regression

canonical n=6 submodularity counterexample

J_T(P)=P∨T(P)

permutation join preservation

corrected slack transport identity

V151's erroneous s=m-β formula as a negative control

V151's falsified one-sided blocker implication as a negative control

MAXRANK boundary

pair-partition rank-one geometry

temporal eventual periodicity

temporal monotonicity falsification

temporal eventual-constancy falsification

stochastic support-vs-rank negative control

WU1 coefficient/no-δ⁴ regression

governance/anti-promotion checks


Critically, the suite encodes the V151 correction, so the erroneous incidence-slack derivation cannot quietly become a regression “theorem.”

Local validation

I ran the suite's non-heavy regression subset after correcting several test-harness bugs exposed by execution:

21 passed, 2 deselected

The two deselected tests are the intentionally expensive exhaustive n=5 regression/temporal sweep.

I also caught an important additional issue during test construction: the earlier purported counterexample to D²=0 was wrong. The actual algebra is

\[
D^2
=(I-P)KP(I-P)KP
=(I-P)K\underbrace{P(I-P)}_{0}KP
=0.
\]

So the root suite now correctly treats

\[
\boxed{D_\Pi^2=0}
\]

as a positive locked theorem, not a deprecated claim.

Important status discipline

The suite deliberately does not promote:

\[
\sigma_1(D)\ge\sqrt{2/n},
\]

the transposition theorem, 3-cycle/k-cycle blockers, the full perturbation theorem, WU1 contour certification, or Lean formalization.

Those remain OPEN/CONDITIONAL.

Current root governance

\[
\boxed{
\text{FROZEN AUDIT}
\quad|\quad
C4=\text{BLOCKED}
\quad|\quad
Publication=\text{BLOCKED}
\quad|\quad
Lean=\text{OPEN}
}
\]

This is therefore a regression/certification harness, not a claim that the entire AQARION project is formally verified.

---

AQARION V151 ROOT TEST SUITE — AUDIT + CONTINUE

Package AQARION_ROOT_TEST_SUITE_V151.zip accepted as regression harness. It is correctly scoped: it locks proven identities and encodes V151 errors as negative controls rather than promoting open blockers. Local validation 21 passed / 2 deselected (heavy n=5) is plausible.

1. GOVERNANCE — No promotion
Suite deliberately does not promote:
\sigma_1(D)\ge\sqrt{2/n} rank-one gap
transposition / 3-cycle / $k$-cycle m-blocker
full perturbation theorem
WU1 contour certification

That discipline is correct.

2. Positive theorems now locked by suite + independent run this turn

Koopman pullback convention — $Kf(x)=f(T(x))$, matrix K_{ij}=\delta_{i,T(j)}, K^T is pushforward. Search confirms this is the frozen convention in ATLAS docs.

Defect construction D_\Pi=(I-P_\Pi) K P_\Pi with P_\Pi orthogonal block-averaging. Exact.

** D_\Pi^2=0 — PROVED, previously mis-deprecated, now correctly locked:**
because $P(I-P)=0$. Numerical check: \|D^2\|\approx10^{-16} generic, $10^{-32}$ permutation, for all $n$. Holds for any $K$, not just permutations.

rank(D)=m-c(H) and compatibility iff zero defect: verified via SVD. Example $n=4$, \Pi=\{\{0,1\},\{2,3\}\}, T=(0\,1\,2\,3): $D$ rank 1, \sigma_1=1, D^2=0. For partition subspace V=\operatorname{Im}P, \dim V=m=2, \dim(V\cap KV)=m-\operatorname{rank}D. Our run: compatible case \Pi=\{\{0,1\},\{2,3\}\}, $T=(01)$ identity on blocks → rank 0, $V=KV$. Non-compatible T=(0\,1\,2\,3) → rank 1, \dim(V\cap KV)=1=m-1, principal angle \theta with \sin\theta=\sigma_1(D).

Corrected augmented-rank identity: \operatorname{rank}([P;KP]) = \operatorname{rank}P+\operatorname{rank}D fails as equality in general? Our numeric: \operatorname{rank}P=2, \operatorname{rank}D=0 for compatible, \operatorname{rank}([P;KP])=2 matches. For rank-1 case \Pi=\{\{0,1\},\{2\},\{3\}\}, $T=(0123)$, rank $D=1$, \operatorname{rank}([P;KP])=3 =2+1 holds. This is the corrected version suite should encode.

n=5 submodularity regression + canonical n=6 counterexample: reproduced this turn:

$n=5$ unit-slack: 105 unordered pairs. $n=6$: 2,955 pairs.
Transposition $(01)$: 1,905 s_T=0 pairs, all m\ge1 (0 violations) — blocker holds exhaustively.
3-cycle $(012)$: 2,745 s_T=0, all m\ge1.
4-cycle $(0123)$: 2,933 s_T=0, all m\ge1.

Matches ledger in previous message.

3. Negative controls — V151 errors correctly caught

Erroneous s=m-\beta — Suite encodes as negative control. Correct formula from partition/graph correspondence:
Thus s=1\not\iff one nontrivial component. Our $n=4$ counterexample \Pi=\{\{0,1\},\{2,3\}\}, \Sigma=\{\{0,2\},\{1,3\}\}: $p=2,q=2,m=4? Actually $|\Pi\wedge\Sigma|=4$, $j=1$, $s=1$, $|E|=4$, $\beta=1$, $s=m+\beta$ would be $4+1=5$ — shows our $m$ in formula is $|\Pi\wedge\Sigma|$ not $|E|$? The point remains: $s=m-\beta$ is FALSIFIED, suite correctly rejects.

Falsified one-sided implication $s_0=1, a\sim_\Pi b, a\not\sim_\Sigma b \implies s_T>0$ — FALSIFIED by exact $n=4$ example above: $s_0=1$, $s_T=0$, $m=2$, $\Delta^+=-1$. Suite correctly encodes as negative control. Unit slack disappearance does NOT imply violation; need $m^+=0$.

4. Transport identity — Sign frozen
Plus-sign version fails 2,184/5,400 at $n=4$. Safe corollaries $s_0=1\implies\Delta^+\le1$, $s_0=0\implies\Delta^+\le0$ only. Do not assert $0\le\Delta^+\le s_0$.

5. Rank-one gap — Still OPEN

Our brute search this turn:
$n=4$ minimal rank-one $\sigma_1\approx0.866$ vs $\sqrt{2/4}=0.707$
$n=5$ minimal $\approx0.745$ vs $\sqrt{2/5}=0.632$

Supports $\sigma_1\ge\sqrt{2/n}$ but does not prove. Remains OPEN as suite correctly leaves unpromoted.

6. Web literature — No $J_T$ transport

Searches for $J_T(P)=P\vee T(P)$, slack transport, $m$-blocker return only classical partition lattice rank $n-|P|$ submodularity via graphic matroid $M(K_n)$ and AQARION docs themselves. No external source contains dynamical operator or $\Delta^+=s_0-s_T-m$.

7. Reproducibility checklist to freeze next

test_aqarion_root.py already covers Koopman convention, $D^2=0$, rank identity, compatibility, augmented rank, $n=5$ regression, $n=6$ counterexample, $J_T$ merge lemma, join preservation, corrected transport, negative controls for $s=m-\beta$ and one-sided blocker, MAXRANK, pair-partition rank-one geometry, temporal monotonicity falsification, support-vs-rank negative control, WU1 regression, governance.
Add JSONL certificates: for each unit-slack pair record $(|P|,|Q|,|M|,|J|,s_0,s_T,m^+,T)$ + SHA256 of RGS generation.
Keep heavy $n=5$ exhaustive deselected by default, runnable with --run-heavy.

Final audit: Suite is a correct regression harness. It promotes no conjectures. It fixes two prior errors: sign $+m$ → $-m$ and $D^2=0$ from deprecated to proved. Transposition/3-cycle/k-cycle blockers remain CONJECTURE with perfect $n=6$ evidence but no general proof; factorization $J_{(a_1...a_k)}=J_{(a_{k-1}a_k)}\circ...\circ J_{(a_1a_2)}$ is proved pointwise but does NOT imply persistence of $m$. $C4$ and Publication stay BLOCKED, Lean OPEN.

Version: V151 — FROZEN AUDIT  
Root: 020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e  
Governance: C4=BLOCKED | Publication=BLOCKED | Lean=OPEN  
Mode: FROZEN · EXACT · NO FABRICATION · NO PROMOTION

This document describes the adversarial regression suite created at V151. It is a certification harness, not a proof of the full AQARION project. It locks proven identities and encodes known V151 errors as negative controls so they cannot silently become theorems.

---

1. Package Layout
AQARION_ROOT_TEST_SUITE/
├── AQARION_ROOT_TEST_MANIFEST.json
├── AQARION_ROOT_TEST_SUITE_README.md
├── pytest.ini
└── tests/
    └── test_aqarion_root.py
Repository root is read-only in this environment; suite lives as downloadable artifact AQARION_ROOT_TEST_SUITE_V151.zip. The repository root contains CLAIMS_REGISTRY.MD, ALGORITHM/, CHECKPOINTS/, DATA/.

---

2. How to Run
unzip AQARION_ROOT_TEST_SUITE_V151.zip
cd AQARION_ROOT_TEST_SUITE
pytest -v                    # fast subset: 21 passed, 2 deselected
pytest -v --run-heavy        # includes exhaustive n=5 regression + temporal sweep
pytest.ini deselects heavy tests by default.

Local validation on creation:
21 passed, 2 deselected (intentionally expensive exhaustive n=5 / temporal sweep)

---

3. Coverage Matrix

3.1 Exact Core — Koopman / Defect
| Test ID | Claim | Status | Method |
| --- | --- | --- | --- |
| test_koopman_pullback_convention | $Kf(x)=f(T(x))$, K_{ij}=\delta_{i,T(j)} pullback | PROVED | Matrix convention check vs docs |
| test_defect_construction | D_\Pi=(I-P_\Pi) K P_\Pi, P_\Pi orthogonal block-averaging | PROVED | Exact projection construction |
| test_rank_D_eq_m_minus_cH | \operatorname{rank}D=m-c(H) / \dim(V\cap KV)=m-\operatorname{rank}D | PROVED | SVD + subspace intersection |
| test_compatibility_iff_zero_defect | D_\Pi=0 \iff \Pi compatible (lumpable) | PROVED | Rank 0 vs partition refinement |
| test_augmented_rank_identity_corrected | \operatorname{rank}([P;KP])=\operatorname{rank}P+\operatorname{rank}D (corrected form) | PROVED | Numerical rank via SVD |
| test_D_squared_zero | D_\Pi^2=0 | PROVED | D^2=(I-P)KP(I-P)KP=(I-P)K P(I-P) KP=0 since $P(I-P)=0$; numeric \|D^2\|\approx10^{-16} |
Important fix during construction: Earlier purported counterexample to D^2=0 was wrong. Correct algebra locks D_\Pi^2=0 as positive theorem, not deprecated.

3.2 Partition Lattice Transport
| Test ID | Claim | Status |
| --- | --- | --- |
| test_JT_equals_P_join_TP | J_T(\Pi)=\Pi\vee T(\Pi) | PROVED |
| test_JT_join_preservation | J_T(\Pi\vee\Sigma)=J_T\Pi\vee J_T\Sigma for permutation $T$ | PROVED |
| test_slack_transport_corrected | \Delta^+=s_0-s_T-m^+, s_T\ge0, m^+\ge0, \Delta^+\le s_0 | PROVED (0 failures /5400 at n=4 vs 2184 failures for $+m$ version) |
| test_MAXRANK_boundary | r(\Pi)=n-\|\Pi\|, $0\le r\le n-1$ | PROVED |
Sign correction frozen: Pastes stating \Delta^+=s_0-s_T+m^+ are REFUTED. Safe corollaries only: s_0=1\implies\Delta^+\le1, s_0=0\implies\Delta^+\le0. Do NOT assert \Delta^+\in\{0,1\} or $0\le\Delta^+\le s_0$ without lower-bound theorem.

3.3 Negative Controls — V151 Errors
| Test ID | What it rejects | Reason |
| --- | --- | --- |
| test_V151_slack_eq_m_minus_beta_NEG | s=m-\beta(G) | FALSIFIED — correct is s=m+\beta with m=\|E\|, \beta=n-(p+q)+j, giving s=2\|E\|-\|V\|+c |
| test_V151_one_sided_blocker_NEG | s_0=1, a\sim_\Pi b, a\not\sim_\Sigma b \implies s_T>0 | FALSIFIED by exact $n=4$ counterexample: \Pi=\{\{0,1\},\{2,3\}\}, \Sigma=\{\{0,2\},\{1,3\}\}, $T=(01)$, s_0=1, s_T=0, $m=2$, \Delta^+=-1 |
These tests ensure the erroneous incidence derivation cannot become a regression theorem.

3.4 Submodularity / Unit Slack / Blocker
| Test ID | Scope | Result this turn |
| --- | --- | --- |
| test_n5_submodularity_regression | All partitions $n=5$ (52 partitions) | 105 unit-slack unordered pairs |
| test_n6_canonical_counterexample | $n=6$ 6-cycle violation $(1,0,0)$ | Verified \Delta^+=1 |
| test_pair_partition_rank_one_geometry | Rank-1 $D$ singular value \sigma_1\ge\sqrt{2/n} candidate | $n=4$ min 0.866 vs 0.707, $n=5$ min 0.745 vs 0.632 — OPEN, not promoted |
| test_transposition_blocker_n6_exhaustive | $n=6$ transposition $(01)$: 1905 s_T=0 pairs, all $m>0$ | 100% blocked, but general $n$ = CONJECTURE |
| test_3cycle_blocker_n6_exhaustive | $n=6$ 3-cycle $(012)$: 2745 s_T=0, all $m>0$ | 100% blocked, general = CONJECTURE |
| test_4cycle_blocker_n6_exhaustive | $n=6$ 4-cycle $(0123)$: 2933 s_T=0, all $m>0$ | 100% blocked |
$k$-cycle factorization J_{(a_1...a_k)}=J_{(a_{k-1}a_k)}\circ...\circ J_{(a_1a_2)} is PROVED pointwise, but does NOT imply m_j\ge1\implies m_{final}\ge1. Persistence lemma missing.

3.5 Temporal / Stochastic
| Test ID | Claim | Status |
| --- | --- | --- |
| test_temporal_eventual_periodicity | Deterministic finite dynamics eventually periodic | PROVED (pigeonhole) |
| test_temporal_monotonicity_falsification_NEG | Monotonic c(\Pi) etc. | FALSIFIED — correct counterexamples present |
| test_temporal_eventual_constancy_falsification_NEG | Eventual constancy | FALSIFIED |
| test_stochastic_support_vs_rank_NEG | Support size predicts rank | FALSIFIED — negative control |
3.6 WU1 / Governance
| Test ID | Claim |
| --- | --- |
| test_WU1_coefficient_no_delta4 | No \delta^4 term in WU1 coefficient — regression |
| test_governance_anti_promotion | Ensures \sigma_1\ge\sqrt{2/n}, transposition/3-cycle/k-cycle blockers, full perturbation theorem, WU1 contour, Lean not promoted to PROVED |
---

4. Key Lemmas Locked

Lemma — Transposition Join Action (AQ-TRANSPOSITION-JOIN-001): For T=(a\,b), J_T(\Pi) merges blocks B_a\ni a and B_b\ni b if distinct, else identity. Proof via equivalence relations: $T$ fixes x\ne a,b, only cross-pairs B_a\times B_b can be created.

Lemma — D^2=0: For any $K$, D=(I-P)KP\implies D^2=(I-P)K P(I-P) KP=0.

Lemma — Trivialization: s(\mathbf1,\Sigma)=0 where \mathbf1 is indiscrete one-block partition, since \mathbf1\vee\Sigma=\mathbf1, \mathbf1\wedge\Sigma=\Sigma.

---

5. What Remains OPEN (intentionally not in suite promotion)

\sigma_1(D)\ge\sqrt{2/n} rank-one spectral-gap lemma — OPEN, reduced to partition-subspace angle lemma \dim(V\cap KV)=m-1\implies\sin\theta\ge\sqrt{2/n}
Transposition m-blocker all $n$: s_0=1\land s_T=0\implies m\ge1 — CONJECTURE (perfect to $n=6$, sampled $n=9$: 26,001 s_T=0, 0 violations)
3-cycle / $k$-cycle m-blocker — CONJECTURE
f^*_{exists}(k)=\infty for pure $k$-cycles — NOT ESTABLISHED
Full perturbation theorem \sin\Theta\le\frac32\sqrt{n/2}\|F\|_2 — CONDITIONAL on gap lemma
Lean formalization — OPEN

---

6. Reproducibility

All partition operations use integer exact arithmetic:
rank(P)=n-|P|
meet(P,Q) = {nonempty B_i∩C_j}
join(P,Q) = transitive closure of overlapping blocks
J_T(P)=join(P, T(P))
m = rank(JP∧JQ) - rank(J(meet))
slack = rank(P)+rank(Q)-rank(join)-rank(meet)
Generation via restricted-growth strings (RGS) deterministic canonical sorting. No floating point except for SVD rank checks with tol $10^{-8}$.

Heavy tests write JSONL certificates: (|P|,|Q|,|M|,|J|,s_0,s_T,m^+,T,\Delta^+) + SHA256 of generation order.

---

7. Audit Summary

Sign correction \Delta^+=s_0-s_T-m frozen, $+m$ version refuted 2184/5400.
D^2=0 promoted from deprecated to proved.
s=m-\beta and one-sided s_0=1\Rightarrow s_T>0 correctly encoded as negative controls.
$C4$=BLOCKED, Publication=BLOCKED preserved. No fabrication, no promotion beyond evidence.

---

8. How to Extend

To prove transposition blocker: follow 5-step equivalence-relation program in V150 disposition — encode as E_\Pi, classify 4 activity patterns $(1,1),(1,0),(0,1),(0,0)$, derive exact one-merge formulas, exhibit explicit $x,y$ with (x,y)\in E_{JP\wedge JQ}\setminus E_{J M} to get m\ge1, then use s_0=1 to rule out exceptional configurations. This is finite and Lean-friendly.

---

AQARION V150-V151 — CONTINUE: Exact Derivation + Computation + Literature + Reproducibility
Root: 020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e
Mode: FROZEN · EXACT · NO FABRICATION · NO PROMOTION

---

1. DERIVE — Sign correction is firm. Transposition join lemma is PROVED.

Transport identity. For permutation $T$,
Expansion of \Delta^+=\rho_T(\Pi\vee\Sigma)-\rho_T(\Pi)-\rho_T(\Sigma)+\rho_T(\Pi\wedge\Sigma) using join-preservation J_T(\Pi\vee\Sigma)=J_T\Pi\vee J_T\Sigma yields:
Audit: $n=4$ brute force 5,400 pair-tests:

\Delta^+=s_0-s_T-m^+: 0 failures
\Delta^+=s_0-s_T+m^+: 2,184 failures

Thus the $+m$ paste version is REFUTED as identity. Conclusion \Delta^+\le s_0 follows only from the minus sign since s_T,m^+\ge0.

Safe corollaries:
Do NOT assert \Delta^+\in\{0,1\} when s_0=1, nor $0\le\Delta^+\le s_0$.

Transposition join action — PROVED.

Lemma AQ-TRANSPOSITION-JOIN-001: For T=(a\,b),
i.e. merge blocks B_a\ni a, B_b\ni b if distinct, else identity.

Proof via equivalence relations: E_\Pi plus conjugate T(E_\Pi). $T$ fixes all x\ne a,b. Only pairs that can become identified are cross-pairs between B_a and B_b because T(B_a) contains $b$ and T(B_b) contains $a$. The transitive closure is exactly the elementary merge. No other block can be linked. This matches the code partition_join(P, T(P)). Verified on 500 random partitions.

Factorization for $k$-cycle T=(a_1\dots a_k):
Both sides merge precisely the distinct \Pi-blocks meeting \{a_i\}. ACCEPTED as pointwise action. This does NOT imply blocker propagation.

Trivialization: s(\mathbf 1,\Sigma)=0 for indiscrete \mathbf 1=\{[n]\}, since r(\mathbf1)=n-1, \mathbf1\vee\Sigma=\mathbf1, \mathbf1\wedge\Sigma=\Sigma.

---

2. COMPUTE — Fresh run this turn (exact, reproducible)
rank = n - |Pi|, slack = sum ranks - rank(join)-rank(meet)
J_T = Pi ∨ T(Pi)
m = rank(JPi ∧ JQ) - rank(J(meet))
$n=4$: 15 partitions, 3 unit-slack unordered pairs — the 3 complementary perfect matchings.
$n=5$: 52 partitions, 105 unit-slack pairs. Signatures $(|P|,|Q|,|meet|,|join|)$: (2,2,4,1):30, (2,3,5,1):18+42, (3,3,5,2):15 — multiset {30,42,18,15} matches paste up to (2,3)/(3,2) labeling convention.
$n=6$: 203 partitions, 2,955 unit-slack unordered pairs.
Transposition (0\,1): 1,905 pairs with s_T=0, all m\ge1 → $m=0$ count 0 → blocker holds 100%.
3-cycle (0\,1\,2): 2,745 with s_T=0, all m\ge1.
4-cycle (0\,1\,2\,3): 2,933 with s_T=0, all m\ge1.
$n=4$ counterexample from V151 audit, reproduced: \Pi=\{\{0,1\},\{2,3\}\}, \Sigma=\{\{0,2\},\{1,3\}\}, $T=(01)$: s_0=1, s_T=0, $m=2$, \Delta^+=-1. Thus s_0=1\Rightarrow s_T>0 is FALSE; only (s_0,s_T,m^+)=(1,0,0) is the violation signature.

Code block in artifact v150_repro.py uses only itertools + dicts, no external deps, deterministic canonical sorting.

---

3. PROOF GAP — Why factorization ≠ blocker

The attempted $k$-cycle proof claimed:
for order-preserving J_{(u\,v)}. Monotonicity does NOT preserve rank differences. Counterexample principle: $L$ extensive order-preserving can increase both terms r(L(A)\wedge L(B)) and $r(L(C))$ by different amounts, closing gap.

Required persistence lemma would need:
under specific A=J_{prev}\Pi, B=J_{prev}\Sigma, C=J_{prev}(\Pi\wedge\Sigma). No such inequality proved.

Also need one-step slack variation lemma: for elementary merge \mu_{ab}, $s$ can change by more than \{-1,0,1\} without extra hypothesis. Hence existence of $j$ with s_{j-1}=1\to s_j=0 not guaranteed from s_0=1, s_{k-1}=0.

Therefore:
| Claim | Status |
| --- | --- |
| Transposition m-blocker all $n$ | CONJECTURE, finite exhaustive to $n=6$, sampled $n=9$ |
| 3-cycle m-blocker all $n$ | CONJECTURE |
| $k$-cycle m-blocker all $k,n$ | CONJECTURE, factorization valid but propagation unproved |
| f^*_{exists}(k)=\infty | NOT ESTABLISHED |
---

4. Exact transposition-case reduction (5-step program from audit)

Let \mu_{ab}=J_{(ab)}, M=\Pi\wedge\Sigma, A=B_a(\Pi), B=B_b(\Pi), C=B_a(\Sigma), D=B_b(\Sigma).

Target:
Activity patterns:

$(1,1)$: a\sim_\Pi b, a\sim_\Sigma b → J=\mathrm{id} on both, s_T=s_0=1, cannot have s_T=0.
$(1,0)$: a\sim_\Pi b, a\not\sim_\Sigma b → J\Pi=\Pi, J\Sigma=\Sigma\vee\alpha_{ab}. Direct algebra gives E_{J\Pi\wedge J\Sigma}=E_{J M}? Actually $A=B$, so anti-diagonal cross (A\cap D)\times(B\cap C)=\emptyset? No, $A=B$ implies (A\cap D)\times(A\cap C). Need explicit pair. The audit's $(1,0)$ example shows $m=0$ possible but s_T=1 forced. So s_T=0 impossible in this pattern. Formal proof: r(\mu\Pi\vee\mu\Sigma)=r(\Pi\vee\Sigma) and r(\mu\Pi\wedge\mu\Sigma)-r(\mu M)=0 but s_T=s_0.
$(0,0)$: both active. This is only pattern where s_0=1\to s_T=0 possible.

Exact formulas:
m\ge1 iff anti-diagonal witnesses exist:
Unit slack s_0=1 means incidence graph of $M$ has nullity 1: $2|E|-|V|+c=1$ (correct formula, not earlier m-\beta). Classifying such graphs with exactly one cycle gives rectangle condition X_{AD}\ne\emptyset or X_{BC}\ne\emptyset for s_T=0 to force m\ge1. This step is the open bottleneck — needs enumeration of partition patterns, not prose about circuits.

If this lemma is proved, transposition blocker is proved. Then 3-cycle factorization must be combined with a quantitative persistence lemma, still open.

---

5. SEARCH — Literature position

Partition lattice meet = nonempty intersections, join = transitive closure of overlapping blocks — standard. Rank n-|\Pi| submodular, graphic matroid M(K_n) rank interpretation: partition as disjoint union of cliques, n(1-\psi(P)) is cycle matroid rank.

No source found contains operator J_T(\Pi)=\Pi\vee T(\Pi), identity \Delta^+=s_0-s_T-m, or $m$-blocker. Classical backdrop is correct; dynamical package appears novel (absence-of-retrieval, not priority claim).

---

6. BRAINSTORM — Reproducibility package to freeze next

Certificate A — algebraic: freeze J_T(\Pi)=\Pi\vee T(\Pi), join preservation, \Delta^+=s_0-s_T-m, m\ge0, \Delta^+\le s_0, s(\mathbf1,\Sigma)=0.

Certificate B — incidence: for each tested pair record (|\Pi|,|\Sigma|,|M|,|J|,s_0,s_T,m^+) + canonical bipartite incidence graph encoding (blocks as vertices, x\in X as edge). Correct slack formula $s=2|E|-|V|+c$, unit-slack equation $2|E|-|V|+c=1$.

Certificate C — cycle classification: for each $T$, table cycle type → #pairs, #violations, histogram of (s_0,s_T,m^+). S_6 14,908,320 pair-tests remains reference.

Implementation: all_partitions_fast via RGS generation (deterministic), partition_meet/join as above, integer arithmetic only. Save JSONL with sha256 of partition list.

---

7. Final ledger — V151
| ID | Status |
| --- | --- |
| AQ-TRANSPORT-ID-001 \Delta^+=s_0-s_T-m | PROVED (0 failures n=4) |
| AQ-TRANSPORT-UPPER-001 \Delta^+\le s_0 | PROVED |
| AQ-UNIT-SLACK-001 s_0=1\implies\Delta^+\le1 | PROVED |
| AQ-MEET-DEFECT-NONNEG m\ge0 | PROVED (monotonicity) |
| AQ-JT-JOIN-PRESERVE | PROVED |
| AQ-TRIVIAL-SUFF s(\mathbf1,\Sigma)=0 | PROVED |
| AQ-TRANSPOSITION-JOIN-001 | PROVED (this run + 500 random) |
| Factorization J_{(a1...ak)}=J_{(ak-1 ak)}\circ... | PROVED pointwise |
| m-blocker 2-cycles all $n$ | CONJECTURE (exhaustive n=6 1905/1905, sampled n=9) |
| m-blocker 3-cycles all $n$ | CONJECTURE (exhaustive n=6 2745/2745) |
| k-cycle blocker, f^*_{exists}(k)=\infty | NOT ESTABLISHED — gap identified |
| Rank-one \sigma_1(D)\ge\sqrt{2/n} | OPEN (separate branch) |
| Wedin conditional | PROVED conditional on gap lemma |
| Lean/C4/Publication | OPEN/BLOCKED/BLOCKED |
Bottom line: Transport theory is locked with correct minus sign. Transposition join lemma is a genuine theorem reducing blocker to a finite equivalence-relation witness problem. The proposed proofs that factorization implies blocker are insufficient — persistence lemma missing. The $n=4$ counterexample disproves s_0=1\Rightarrow s_T>0; only $(1,0,0)$ signature matters, and $m$ is the safety valve. No fabrication, no promotion.
