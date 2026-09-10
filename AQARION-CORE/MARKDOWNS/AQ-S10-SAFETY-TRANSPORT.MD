AQARION — Transport-Safety Continuation Audit

September 10, 2026

Mode: FROZEN · EXACT · ADVERSARIAL · NO PROMOTION

Root: 020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284

Governance: C4 BLOCKED · Publication BLOCKED · Lean OPEN · SDS-002 FROZEN/QUARANTINED · EK-001 QUARANTINED

I continued the attack rather than accepting the proposed \(n=14\) fixture on sight. I independently reconstructed its partition operations and found an important notation trap, but not a mathematical failure:

the block-count expression \(|P|+|Q|-|M|-|U|\) is \(-1\);

the actual \(s_0\) used by the transport theory is the rank-equivalent quantity


\[
  s_0=|M|+|U|-|P|-|Q|=1.
\]

\[
  s_T=|J_T(M)|+|J_T(U)|-|J_T(P)|-|J_T(Q)|.
\]

With that convention, the \(n=14\) fixture does verify exactly.

This is worth locking because the sign convention is precisely the kind of error that previously produced SDS-002.


---

Independent verification of the \(n=14\) fixture

Using the supplied \(P,Q\), I independently reconstructed:

\[
|P|=4,\qquad |Q|=6,\qquad |M|=10,\qquad |U|=1.
\]

Therefore

\[
s_0
=
|M|+|U|-|P|-|Q|
=
10+1-4-6
=
1.
\]

The closures reconstruct exactly as supplied:

\[
|J_T(P)|=2,\qquad
|J_T(Q)|=4,\qquad
|J_T(M)|=8,\qquad
|J_T(U)|=1.
\]

The rank-defect convention gives

\[
d_P=4-2=2,
\]

\[
d_Q=6-4=2,
\]

\[
d_M=10-8=2,
\]

\[
d_U=1-1=0.
\]

Thus

\[
\Delta=2+2-2-0=2.
\]

And

\[
s_T
=
8+1-2-4
=
3.
\]

Hence

\[
\boxed{s_T-s_0=3-1=2}.
\]

The marked-block calculation independently gives

\[
q_S(P)=3,\qquad
q_S(Q)=3,\qquad
q_S(M)=3,\qquad
q_S(U)=1,
\]

so

\[
\kappa_S=3+3-3-1=2.
\]

Finally,

\[
J_T(M)=J_T(P)\wedge J_T(Q),
\]

so

\[
m_T=0.
\]

Therefore the fixture satisfies

\[
\boxed{
s_0=1,\quad
m_T=0,\quad
\kappa_S=2,\quad
\Delta=2,\quad
s_T=3.
}
\]

This independently confirms that the upper endpoint is actually attained.

Adversarial sign finding

The raw block-count expression

\[
|P|+|Q|-|M|-|U|
\]

must not be used as \(s_0\).

The correct identity is

\[
\boxed{
s_0
=
r_P+r_Q-r_M-r_U
=
|M|+|U|-|P|-|Q|
}
\]

for

\[
r_R=n-|R|.
\]

Similarly,

\[
\boxed{
d_T(R)=r_{J_T(R)}-r_R=|R|-|J_T(R)|.
}
\]

This is exactly the sign convention that makes

\[
s_T=s_0+\Delta+m_T.
\]

I recommend making this an explicit regression assertion in the source rather than relying on naming conventions.


---

The two sharp fixtures are now established

The transport spectrum has explicit witnesses at both nontrivial values:

Fixture	\(s_0\)	\(m_T\)	\(\kappa_S\)	\(\Delta\)	\(s_T\)

\(n=8\)	1	0	1	1	2
\(n=14\)	1	0	2	2	3


Thus the proved range

\[
0\le\Delta\le2
\]

is sharp at both ends of its nonzero part.

The \(n=8\) fixture rejects

\[
\Delta=0.
\]

The \(n=14\) fixture rejects

\[
\Delta\le1.
\]

Therefore the previous conjectural strengthening

\[
m_T=0\Rightarrow\Delta\le1
\]

is now definitively REFUTED.

The surviving theorem is exactly:

\[
\boxed{
m_T=0
\Longrightarrow
\Delta=\kappa_S
\in\{0,1,2\}.
}
\]


---

The three-lemma proof is the correct core

The proposed compression is sound. I would freeze the mathematical proof around three substantive lemmas rather than a larger architecture.

Closure-loss lemma

For

\[
S=\{0,1,2\}
\]

and

\[
q_S(R)=|\{B\in R:B\cap S\ne\varnothing\}|,
\]

the action of \(T=(012)\) changes only blocks touching \(S\).

Consequently,

\[
\boxed{
d_T(R)=q_S(R)-q_S(J_T(R)).
}
\]

This follows because all blocks disjoint from \(S\) are fixed individually by \(T\), while the blocks meeting \(S\) are replaced by their orbit-generated identifications.

Therefore

\[
\begin{aligned}
\Delta
&=
d_T(P)+d_T(Q)-d_T(M)-d_T(U)\\
&=
\kappa_S(P,Q)
-
\kappa_S(J_T(P),J_T(Q)),
\end{aligned}
\]

once the meet and join terms are transported appropriately.


---

Invariant-\(\kappa\) lemma

If \(R\) is \(T\)-invariant, then a block meeting \(S\) is either

\[
S\subseteq B
\]

or

\[
B=\{s\}
\]

for a single \(s\in S\).

The proof is local: if a block contains two points of the \(T\)-orbit, its translates overlap, hence coincide, forcing all three points into the block. If it contains one marked point and an outside fixed point, the same fixed outside point occurs in all translates, again forcing coincidence.

Thus an invariant partition has exactly one of:

\[
q_S(R)=1
\]

or

\[
q_S(R)=3.
\]

For two invariant partitions, the four cases are:

\[
(1,1),\ (1,3),\ (3,1),\ (3,3).
\]

Their meet/join marked-block counts give:

\[
\kappa_S=0
\]

in every case.

Hence

\[
\boxed{
R,W\text{ \(T\)-invariant}
\Longrightarrow
\kappa_S(R,W)=0.
}
\]

This is the key local theorem.


---

Meet-transport lemma

Let

\[
M=P\wedge Q.
\]

The meet defect is

\[
m_T
=
r_{J_T(M)}
-
r_{J_T(P)\wedge J_T(Q)}.
\]

Because

\[
J_T(M)\preceq J_T(P)\wedge J_T(Q),
\]

\(m_T=0\) implies equality of the two partitions, not merely equality of their ranks:

\[
\boxed{
m_T=0
\Longrightarrow
J_T(M)=J_T(P)\wedge J_T(Q).
}
\]

Also \(J_T\) preserves joins:

\[
J_T(U)=J_T(P)\vee J_T(Q).
\]

Therefore the second marked-incidence bracket becomes

\[
\kappa_S(J_T(P),J_T(Q)),
\]

which vanishes by the invariant-\(\kappa\) lemma.

Thus:

\[
\boxed{
m_T=0
\Longrightarrow
\Delta=\kappa_S(P,Q).
}
\]

That is the central theorem.


---

The graph bound is independent and exact

Construct the marked incidence graph from the three elements of \(S\).

It has exactly three marked edges.

Because the graph is bipartite and simple, a cycle requires at least four edges.

Therefore

\[
\beta(H_S)=0.
\]

The exact incidence identity is

\[
\kappa_S
=
c(H_S)-c_G^{\mathrm{touched}}.
\]

Since

\[
1\le c_G^{\mathrm{touched}}
\le c(H_S)\le3,
\]

we get

\[
0\le\kappa_S\le2.
\]

Hence

\[
\boxed{
m_T=0
\Longrightarrow
0\le\Delta=\kappa_S\le2.
}
\]

And therefore

\[
\boxed{
s_T-s_0=\kappa_S\ge0.
}
\]

The particularly clean theorem statement is:

\[
\boxed{
m_T=0
\Longrightarrow
s_T-s_0=\kappa_S
\in\{0,1,2\}.
}
\]

The \(n=8\) and \(n=14\) fixtures show that both \(1\) and \(2\) actually occur.


---

A useful interpretation emerges

This gives the transport quantity a much better meaning than simple monotonicity.

Under meet preservation,

\[
\boxed{
s_T-s_0=\kappa_S.
}
\]

So the increase in the incidence-cycle statistic is exactly the number of marked-incidence components that become connected only after the unmarked ambient incidence edges are restored.

For three marked edges:

\(\kappa_S=0\): no increase;

\(\kappa_S=1\): one unit of transport increase;

\(\kappa_S=2\): maximal transport increase.


The \(n=8\) fixture realizes the middle case.

The \(n=14\) fixture realizes the maximum.

That is a much more informative theorem than merely

\[
s_T\ge s_0.
\]


---

The remaining proof obligation is now genuinely small

There is no remaining mathematical uncertainty about the bound.

The only substantial formal work is expressing the above three lemmas in the actual partition definitions.

The dependency graph should be:

partition lattice
      │
      ├── meet / join
      │
      └── T-action
             │
             ▼
       orbit closure J_T
             │
      ┌──────┴────────┐
      ▼               ▼
closure-loss      invariant blocks
      │               │
      └──────┬────────┘
             ▼
       marked κ identity
             │
             ▼
      m_T = 0 transport
             │
             ▼
        Δ = κ_S
             │
             ▼
       0 ≤ κ_S ≤ 2
             │
             ▼
        s_T ≥ s_0

This is now small enough that I would not build the entire old C3 machinery first.

Formalize the three lemmas directly.


---

Regression assertions that should be frozen

The sign issue uncovered during independent verification deserves an explicit machine-level invariant.

rank(R) = n - |R|

s0 =
  rank(P) + rank(Q)
  - rank(M) - rank(U)

  =
  |M| + |U| - |P| - |Q|

dT(R) =
  rank(JT(R)) - rank(R)

  =
  |R| - |JT(R)|

sT =
  rank(JP) + rank(JQ)
  - rank(JM) - rank(JU)

Delta =
  dP + dQ - dM - dU

mT =
  rank(JM)
  - rank(JP ∧ JQ)

Then assert:

\[
\boxed{s_T=s_0+\Delta+m_T.}
\]

This would have caught the sign ambiguity immediately.

I would add this as a precondition check to the evidence kernel rather than letting downstream computations discover it.


---

Fixture records

The verified regression records should now be:

{
  "fixture": "C3-TRANSPORT-N8",
  "n": 8,
  "T": [0,1,2],
  "s0": 1,
  "mT": 0,
  "kappaS": 1,
  "d": [1,1,1,0],
  "Delta": 1,
  "sT": 2,
  "status": "VERIFIED",
  "purpose": "rejects_Delta_zero"
}

and

{
  "fixture": "C3-TRANSPORT-N14",
  "n": 14,
  "T": [0,1,2],
  "s0": 1,
  "mT": 0,
  "kappaS": 2,
  "d": [2,2,2,0],
  "Delta": 2,
  "sT": 3,
  "status": "VERIFIED",
  "purpose": "rejects_Delta_le_one"
}

I would also store the full \(P,Q,M,U,JP,JQ,JM,JU\) arrays in both records, rather than relying on derived scalars.

Do not overwrite the historical quarantined fixture. Add these as independently verified regression records.


---

Literature check

The linked paper is directly relevant to the methodological positioning. Coote and Colbrook state that finite EDMD matrices always have eigenvalues, while many computed eigenvalues may not correspond to the underlying infinite-dimensional Koopman operator; they therefore use residuals as a posteriori diagnostics and combine that with conditioning requirements. 

That supports the AQARION principle:

\[
\text{computed representation}
\neq
\text{certified structural object}.
\]

It does not prove the transport theorem.

The partition-lattice literature is also a particularly good fit. Anagnostopoulou-Merkouri, Bailey, and Cameron prove that invariant partitions under a finite transitive permutation group form a sublattice of the partition lattice. 

But the distinction remains important:

\[
\text{invariant partitions form a sublattice}
\]

does not imply

\[
J_T(P\wedge Q)=J_T(P)\wedge J_T(Q)
\]

for arbitrary \(P,Q\). The latter is precisely the additional \(m_T=0\) hypothesis in AQARION.

The behavioral-refinement connection is also legitimate. Groote and Jansen's CONCUR 2025 work gives an \(O(m\log n)\) partitioning algorithm for branching bisimulation and explicitly uses block splitting/refinement.  This supports the refinement/certification context, not the C3 theorem itself.

Finally, the official Provenance Run Crate profile really is version \(0.6\), explicitly describing internal step executions and intermediate outputs, with datePublished = 2024-06-19.  That remains strong architectural support for the AQARION provenance model, while the date must not be conflated with a later repository/record update.


---

Updated theorem ledger

Established mathematically

\[
J_T\text{ extensive}
\]

\[
J_T\text{ monotone}
\]

\[
J_T^2=J_T
\]

\[
J_T(P\vee Q)=J_T(P)\vee J_T(Q)
\]

\[
s_0=|M|+|U|-|P|-|Q|
\]

\[
d_T(R)=|R|-|J_T(R)|
\]

\[
d_T(R)=q_S(R)-q_S(J_T(R))
\]

\[
m_T=0
\Rightarrow
J_T(M)=J_T(P)\wedge J_T(Q)
\]

\[
T\text{-invariant }R,W
\Rightarrow
\kappa_S(R,W)=0
\]

\[
m_T=0
\Rightarrow
\Delta=\kappa_S
\]

\[
0\le\kappa_S\le2
\]

\[
m_T=0
\Rightarrow
0\le\Delta\le2
\]

\[
m_T=0
\Rightarrow
s_T-s_0=\kappa_S
\]

\[
m_T=0
\Rightarrow
s_T\ge s_0.
\]

Explicitly refuted

\[
m_T=0\Rightarrow\Delta=0
\]

\[
m_T=0\Rightarrow\Delta\le1
\]

\[
\kappa_S=2\Rightarrow m_T>0
\]

\[
s_0=1\land m_T=0\Rightarrow s_T=1.
\]

Verified regression fixtures

\[
(n,\Delta,\kappa_S)=(8,1,1)
\]

\[
(n,\Delta,\kappa_S)=(14,2,2).
\]

Still formally open

actual Lean definitions;

Lean proof of closure-loss lemma;

Lean proof of invariant-\(\kappa\) lemma;

Lean proof that \(m_T=0\) yields meet equality;

Lean proof of \(\Delta=\kappa_S\);

Lean proof of the three-edge forest bound;

#print axioms;

zero-sorryAx audit;

nanoda receipt;

independent Lean certificate.



---

Evidence status

Component	Status

Transport theorem mathematically	PROVED
Upper bound \(2\)	PROVED
Sharpness at \(1\)	VERIFIED FIXTURE
Sharpness at \(2\)	VERIFIED FIXTURE
\(n=14\) full witness reconstruction	INDEPENDENTLY CHECKED
Sign convention	LOCKED / REGRESSION REQUIRED
Lean formalization	OPEN
Lean receipt	ABSENT
#print axioms	ABSENT
zero-sorry audit	ABSENT
EK-001	QUARANTINED
SDS-002	FROZEN / QUARANTINED
C4	BLOCKED
Publication	BLOCKED



---

Adversarial conclusion

The \(n=14\) fixture survives independent reconstruction, with one important correction to the presentation of the rank/sign convention.

The actual verified endpoint is:

\[
\boxed{
s_0=1,\quad
m_T=0,\quad
\kappa_S=2,\quad
\Delta=2,\quad
s_T=3.
}
\]

Therefore the transport spectrum is genuinely sharp:

\[
\boxed{
s_T-s_0=\kappa_S\in\{0,1,2\}.
}
\]

The \(n=8\) and \(n=14\) witnesses establish the two nonzero levels:

\[
1,\quad2.
\]

The correct theorem is therefore no longer a conjectural inequality but the exact structural identity

\[
\boxed{
m_T=0
\Longrightarrow
\Delta=\kappa_S,
\qquad
0\le\kappa_S\le2.
}
\]

The highest-value next step is formal proof of the three local lemmas, not another census.

One thing should be added to the frozen regression suite immediately: an assertion that all implementations use

\[
s_0=|M|+|U|-|P|-|Q|
\]

and

\[
d_T(R)=|R|-|J_T(R)|.
\]

The independent reconstruction shows why that is not cosmetic: reversing the block-count expression produces exactly the kind of false contradiction that SDS-002 was designed to expose.

No C4. No publication promotion. No invented Lean receipt. No further search for an upper witness. The mathematical target is now sharply isolated and the endpoint is experimentally realized.Worked for 1m 54s

Yes. I continued the attack, and the important result is that the transport route survives a stronger adversarial pass. There is also one useful upgrade: the previously quarantined \(n=14\) fixture can now be reconstructed and independently checked from the complete \(P,Q\) data available in the audit record. So it can move from “claimed/unverified” to verified regression fixture.

I would make the following the new frozen state.

AQARION — Transport-Safety Continuation Audit

September 10, 2026

Mode: FROZEN · EXACT · NO FABRICATION · NO PROMOTION

Root:
020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e

Governance:
C4 BLOCKED · Publication BLOCKED · Lean OPEN · SDS-002 FROZEN/QUARANTINED · EK-001 QUARANTINED

Doctrine:
EXECUTION ≠ EVIDENCE ≠ PROOF


---

Major result

The proposed stronger bounds are permanently dead:

\[
\Delta=0
\]

is false,

\[
\Delta\le1
\]

is false, and

\[
\kappa_S=2\Longrightarrow m_T>0
\]

is false.

The correct structural target is:

\[
\boxed{
m_T=0
\Longrightarrow
\Delta=\kappa_S
\Longrightarrow
0\le\Delta\le2
\Longrightarrow
s_T\ge s_0.
}
\]

The new point is that the upper endpoint is now independently reconstructed.


---

The \(n=14\), \(\Delta=2\) fixture is verified

Take

\[
X=\{0,\ldots,13\},
\qquad T=(012).
\]

Define

\[
P=
\{
\{0,7,10\},
\{1,3,6\},
\{2,8,9\},
\{4,5,11,12,13\}
\}
\]

and

\[
Q=
\{
\{0,4,10\},
\{1,3\},
\{2,9\},
\{5,6\},
\{7,11\},
\{8,12,13\}
\}.
\]

Direct independent recomputation gives

\[
M=P\wedge Q
=
\{
\{0,10\},
\{1,3\},
\{2,9\},
\{4\},
\{5\},
\{6\},
\{7\},
\{8\},
\{11\},
\{12,13\}
\}
\]

and

\[
U=P\vee Q=X.
\]

Hence

\[
|P|=4,\quad |Q|=6,\quad |M|=10,\quad |U|=1
\]

and therefore

\[
s_0=10+1-4-6=1.
\]

The closures are

\[
J_T(P)=
\{
\{0,1,2,3,6,7,8,9,10\},
\{4,5,11,12,13\}
\},
\]

\[
J_T(Q)=
\{
\{0,1,2,3,4,9,10\},
\{5,6\},
\{7,11\},
\{8,12,13\}
\},
\]

\[
J_T(M)=
\{
\{0,1,2,3,9,10\},
\{4\},
\{5\},
\{6\},
\{7\},
\{8\},
\{11\},
\{12,13\}
\}.
\]

And independently:

\[
J_T(M)=J_T(P)\wedge J_T(Q),
\]

so

\[
m_T=0.
\]

The closure losses are

\[
d_P=2,\qquad d_Q=2,\qquad d_M=2,\qquad d_U=0.
\]

Therefore

\[
\boxed{\Delta=2+2-2-0=2}.
\]

The marked-component calculation gives

\[
q_S(P)=q_S(Q)=q_S(M)=3,\qquad q_S(U)=1,
\]

so

\[
\kappa_S=3+3-3-1=2.
\]

Thus

\[
\boxed{
s_0=1,\quad m_T=0,\quad
\kappa_S=2,\quad
\Delta=2,\quad
s_T=3.
}
\]

The marked graph consists of the three edges

\[
( P_0,Q_0),\quad(P_1,Q_1),\quad(P_2,Q_2),
\]

so

\[
c(H_S)=3,\qquad
c_G^{\rm touched}=1,\qquad
\beta(H_S)=0,
\]

giving

\[
\kappa_S=3-1=2.
\]

This is now a genuine adversarial regression fixture.

Fixture ledger

Fixture	\(s_0\)	\(m_T\)	\(\kappa_S\)	\(\Delta\)	Status

\(n=8\)	1	0	1	1	VERIFIED
\(n=14\)	1	0	2	2	VERIFIED


So the upper bound is not merely plausible:

\[
\boxed{0\le\Delta\le2}
\]

is sharp at both endpoints above and below.

The \(n=8\) fixture kills accidental equality.
The \(n=14\) fixture kills accidental \(\Delta\le1\).


---

The central proof can be compressed further

I agree with the proposed five-lemma decomposition, but after working through it I think we can reduce the mathematical core to three actual lemmas.

The crucial observation is that the \(m_T=0\) condition itself supplies the only meet statement we need.

Let

\[
M=P\wedge Q,\qquad
U=P\vee Q.
\]

Define

\[
d_T(R)=|R|-|J_T(R)|
\]

and

\[
q_S(R)=\#\{B\in R:B\cap S\neq\varnothing\}.
\]

Because \(J_T\) only identifies blocks belonging to the \(T\)-orbit of blocks meeting \(S\),

\[
\boxed{
d_T(R)=q_S(R)-q_S(J_T(R)).
}
\]

This is the closure-loss lemma.

Then

\[
\begin{aligned}
\Delta
&=d_T(P)+d_T(Q)-d_T(M)-d_T(U)\\
&=
[q_S(P)+q_S(Q)-q_S(M)-q_S(U)]\\
&\quad-
[q_S(JP)+q_S(JQ)-q_S(JM)-q_S(JU)].
\end{aligned}
\]

The first bracket is exactly

\[
\kappa_S(P,Q).
\]

Since \(J_T\) preserves joins,

\[
J_T(U)=J_T(P)\vee J_T(Q).
\]

If \(m_T=0\),

\[
|J_T(M)|
=
|J_T(P)\wedge J_T(Q)|.
\]

Since

\[
J_T(M)\preceq J_T(P)\wedge J_T(Q),
\]

equal cardinality implies equality:

\[
\boxed{
m_T=0
\Longrightarrow
J_T(M)=J_T(P)\wedge J_T(Q).
}
\]

Therefore the second bracket is

\[
\kappa_S(J_T(P),J_T(Q)).
\]

So:

\[
\boxed{
m_T=0
\Longrightarrow
\Delta=
\kappa_S(P,Q)-\kappa_S(JP,JQ).
}
\]

That part is now purely algebraic.

The only remaining mathematical input is therefore:

\[
\boxed{
P,Q\text{ \(T\)-invariant}
\Longrightarrow
\kappa_S(P,Q)=0.
}
\]

And this lemma is extremely small.


---

Invariant-\(\kappa\) lemma

For a \(T=(012)\)-invariant partition, the marked points have exactly two possible configurations.

Type I

\[
0,1,2
\]

belong to one common block.

Thus

\[
q_S=1.
\]

Type II

\[
\{0\},\{1\},\{2\}
\]

are three singleton blocks.

Thus

\[
q_S=3.
\]

No other configuration is possible.

In particular, a \(T\)-invariant block cannot contain exactly two marked elements, and a block containing one marked element plus an unmarked element would generate three distinct translates that intersect improperly.

Now there are only four cases.

\(JP\)	\(JQ\)	\(q_S(JP)\)	\(q_S(JQ)\)	\(q_S(JP\wedge JQ)\)	\(q_S(JP\vee JQ)\)	\(\kappa_S\)

I	I	1	1	1	1	0
I	II	1	3	3	1	0
II	I	3	1	3	1	0
II	II	3	3	3	3	0


Hence

\[
\boxed{\kappa_S(JP,JQ)=0}.
\]

Consequently:

\[
\boxed{
m_T=0\Longrightarrow\Delta=\kappa_S(P,Q).
}
\]

This is the central transport theorem.

I would now regard the proof as mathematically highly constrained but formally OPEN until written in the actual partition definitions and checked independently.


---

The upper bound is now almost embarrassingly local

The incidence graph \(H_S\) has at most three marked edges.

It is bipartite.

It is simple: two distinct meet blocks cannot correspond to the same pair of \(P\)- and \(Q\)-blocks.

A nontrivial cycle in a simple bipartite graph has at least four edges. Therefore

\[
|E(H_S)|\le3
\Longrightarrow
\beta(H_S)=0.
\]

Hence

\[
\kappa_S
=
c(H_S)-c_G^{\rm touched}.
\]

Because

\[
1\le c_G^{\rm touched}
\le c(H_S)
\le3,
\]

we obtain

\[
\boxed{0\le\kappa_S\le2}.
\]

Together with the transport lemma:

\[
\boxed{
m_T=0
\Longrightarrow
0\le\Delta\le2.
}
\]

And therefore, from

\[
s_T=s_0+\Delta+m_T,
\]

\[
m_T=0
\Longrightarrow
s_T=s_0+\kappa_S
\ge s_0.
\]

So the strongest clean formulation is actually:

\[
\boxed{
m_T=0
\Longrightarrow
s_T-s_0=\kappa_S
\in\{0,1,2\}.
}
\]

That is substantially better than merely saying \(s_T\ge s_0\).


---

Important conceptual upgrade

I would make

\[
\boxed{s_T-s_0=\kappa_S}
\]

the headline transport equation under meet preservation.

The theorem is not merely a monotonicity statement.

It says the entire transport increase is exactly the number of marked incidence components that are fused through the ambient incidence graph.

So:

\(\kappa_S=0\): no cycle-rank transport increase;

\(\kappa_S=1\): one unit of increase;

\(\kappa_S=2\): maximal possible increase for a three-point support.


The two fixtures now realize the nontrivial cases:

\[
1\mapsto1,
\qquad
2\mapsto2.
\]

The \(0\)-case is of course realized by the many \(E=0\) computational cases.

This gives a very clean calibration of the theorem.


---

Adversarial computation

The evidence ledger should now be updated to:

Test	Result	Status

Local \(d_T\) classification, \(n=3,\ldots,9\)	0 failures	COMPUTATIONALLY VERIFIED
\(m_T=0\), \(n=6\)	8,008 cases, \(E=0\)	COMPUTATIONALLY VERIFIED
\(m_T=0\), \(n=7\)	124,143 cases, \(E=0\)	COMPUTATIONALLY VERIFIED
\(n=8\) fixture	\(\Delta=\kappa_S=1\)	VERIFIED
\(n=14\) fixture	\(\Delta=\kappa_S=2\)	VERIFIED
\(m_T=0\Rightarrow\Delta=\kappa_S\)	proof not formalized	OPEN
\(\Delta\le1\)	explicit counterexample	REFUTED
\(\Delta=0\)	explicit counterexample	REFUTED
\(\kappa_S=2\Rightarrow m_T>0\)	explicit counterexample	REFUTED


The computational \(n=6,n=7\) checks are supporting evidence, not proof.

No \(n=8\) exhaustive pair census is being claimed.

No \(n=9\) pair census is being claimed.


---

The loss-pattern table changes role

I agree with retaining

\[
L(P,Q)=(d_P,d_Q,d_M,d_U).
\]

But I would now use it primarily as a formal regression oracle, rather than the mathematical proof engine.

There are only

\[
3^4=81
\]

raw vectors.

The important derived quantity is

\[
E=\Delta-\kappa_S.
\]

The entire attack becomes:

\[
\boxed{
E(L,\text{incidence type})=0?
}
\]

The \(n=6\) and \(n=7\) exact tests found no \(E\neq0\).

The proof explains why, if the invariant-\(\kappa\) lemma and the closure-loss lemma are correct.

This is much stronger than merely observing a census pattern.


---

One subtle point worth locking

Do not state that “the invariant partitions form a sublattice” as if that proves the AQARION meet statement.

The 2025 Forum of Mathematics, Sigma paper by Anagnostopoulou-Merkouri, Bailey, and Cameron explicitly establishes that \(G\)-invariant partitions form a sublattice in their setting. 

But your \(J_T\) is a specific closure operator, and the question is stronger/different:

\[
J_T(P\wedge Q)
=
J_T(P)\wedge J_T(Q)
\]

for this particular pair.

That equality is exactly what \(m_T=0\) supplies. The sublattice fact does not magically imply that an arbitrary closure onto the invariant sublattice preserves meets.

That distinction is worth preserving in the paper.

There is also a useful conceptual connection to orbit-closure literature: orbit closures of permutation groups and their relation to invariant relations are established subjects, but those closures concern the group/action itself rather than this particular partition-lattice transport functional. 

So AQARION should not claim novelty merely for “using orbit closure.” The potentially distinctive object is the marked incidence transport defect.


---

Lean architecture

I would now make the formal development exactly this small:

Closure layer

Prove

\[
d_T(R)=q_S(R)-q_S(J_T(R)).
\]

Then prove the marked configuration classification.

Invariant layer

Prove

\[
T\text{-Invariant}(P)
\land
T\text{-Invariant}(Q)
\Longrightarrow
\kappa_S(P,Q)=0.
\]

This is the four-case theorem above.

Transport layer

Prove

\[
m_T=0
\Longrightarrow
J_T(P\wedge Q)=J_T(P)\wedge J_T(Q),
\]

then algebraically derive

\[
\boxed{\Delta=\kappa_S}.
\]

Graph layer

Prove

\[
|E(H_S)|\le3
\Longrightarrow
\beta(H_S)=0.
\]

Mathlib currently has the bipartite-simple-graph infrastructure needed to represent \(H_S\), including SimpleGraph.IsBipartiteWith and SimpleGraph.IsBipartite. 

I would still not depend on a high-level “bipartite implies girth ≥4” theorem. The robust Lean route is the finite support argument:

\[
|E|\le3
\]

plus bipartiteness plus simplicity directly implies no cycle.

That minimizes dependence on library theorem names and version drift.

Lean 4.33.1 itself remains an official release dated August 21, 2026. 


---

New formalization target

The first serious Lean target should therefore be:

\[
\boxed{
\texttt{transport\_delta\_eq\_kappa}
}
\]

with assumptions expressing only:

1. \(J\) preserves joins;


2. \(m_T=0\);


3. \(J(P),J(Q)\) are \(T\)-invariant;


4. closure loss is represented by \(q_S-q_S\circ J\);


5. invariant pairs have zero \(\kappa_S\).



Then the proof should be essentially simp/rewriting followed by ring arithmetic.

That is much safer than encoding the whole C3 construction at once.


---

Regression fixture specification

The machine-readable regression object should contain both fixtures.

C3-TRANSPORT-FIXTURE-N8
n: 8
T: (0 1 2)
s0: 1
mT: 0
dP: 1
dQ: 1
dM: 1
dU: 0
kappaS: 1
Delta: 1
E: 0
status: VERIFIED
purpose:
  rejects Delta=0

and

C3-TRANSPORT-FIXTURE-N14
n: 14
T: (0 1 2)
s0: 1
mT: 0
dP: 2
dQ: 2
dM: 2
dU: 0
kappaS: 2
Delta: 2
E: 0
status: VERIFIED
purpose:
  rejects Delta<=1

The second fixture is now legitimate because the full \(P,Q\) data have been independently reconstructed and evaluated.

Do not overwrite the historical quarantined artifact. Add the verified fixture as a new audit record.


---

Provenance / evidence status

No mathematical status changes should be inferred from the provenance work.

The current Provenance Run Crate 0.6 record is indeed dated September 7, 2026 and explicitly describes workflow execution, internal step executions, and intermediate outputs. 

That is useful for the evidence-kernel architecture, but it does not certify the transport theorem.

Likewise the current Lean release being 4.33.1 does not constitute an AQARION Lean receipt. 

So:

Lean receipt: ABSENT

#check receipt: ABSENT

#print axioms: ABSENT

zero-sorry receipt: ABSENT

Lean SHA-256 certificate: ABSENT

EK-001: QUARANTINED

SDS-002: FROZEN / QUARANTINED

C4: BLOCKED

publication promotion: BLOCKED


No change there.


---

Recent literature positioning

There is a useful methodological connection to current partition-refinement work as well. Groote and Jansen's CONCUR 2025 paper gives an \(O(m\log n)\) state-based algorithm for branching bisimulation using block splitting/refinement. 

That supports the broader AQARION theme of treating partitions as behavioral objects that are refined and certified, but it should remain background rather than evidence for C3.

The newer invariant-partition literature is more directly relevant: the 2025 Forum of Mathematics, Sigma paper places invariant partitions explicitly inside partition-lattice/block-structure theory. 

The AQARION distinction should be:

\[
\text{invariant-partition lattice structure}
\]

versus

\[
\text{specific closure-induced transport identity}.
\]

That is the mathematically clean positioning.


---

Frozen hierarchy

I would now lock this:

\[
\boxed{
\begin{array}{c}
J_T\text{ is a closure operator}\\
\downarrow\\
m_T=0\text{ gives meet preservation for the selected pair}\\
\downarrow\\
\Delta=\kappa_S\\
\downarrow\\
0\le\kappa_S\le2\\
\downarrow\\
0\le\Delta\le2\\
\downarrow\\
s_T-s_0=\kappa_S\\
\downarrow\\
s_T\ge s_0
\end{array}}
\]

with the epistemic boundary:

\[
\boxed{
\Delta=\kappa_S
\quad\text{FORMALLY OPEN}
}
\]

but with its proof now reduced to a small, explicit collection of lemmas.

And the sharpness fixtures are:

\[
\boxed{\Delta=1\text{ at }n=8}
\]

and

\[
\boxed{\Delta=2\text{ at }n=14}.
\]


---

Adversarial conclusion

This continuation strengthens the transport-safety program.

The failed upper-bound route is now genuinely dead rather than merely abandoned. The \(n=14\) reconstruction demonstrates that the bound \(2\) is actually attained:

\[
m_T=0,\qquad
s_0=1,\qquad
\Delta=\kappa_S=2,\qquad
s_T=3.
\]

The remaining theorem is no longer “find the right numerical bound.” The bound is known and sharp.

The real bottleneck is now exactly:

\[
\boxed{
m_T=0\Longrightarrow\Delta=\kappa_S.
}
\]

And importantly, the proposed proof does not require another giant census.

The highest-value next action is therefore to formalize/attack:

\[
\boxed{
\begin{aligned}
d_T(R)&=q_S(R)-q_S(J_T(R)),\\
T\text{-Invariant}(P,Q)&\Rightarrow\kappa_S(P,Q)=0,\\
m_T=0&\Rightarrow J_T(P\wedge Q)=J_T(P)\wedge J_T(Q),\\
&\Rightarrow\Delta=\kappa_S.
\end{aligned}}
\]

Then separately certify the three-edge graph lemma.

**No C4. No publication promotion. No invented Lean receipt. No resurrection of \(\Delta\le1\). No further brute-force search for an \(n=14\) witness—the upper fixture is now independently verified.**

AQARION — Transport-Safety Continuation Audit


September 10, 2026


Mode: FROZEN · EXACT · ADVERSARIAL · NO PROMOTION


Root:


020a9110088010116075e1812c98bcd2bcc4905367fa8943a68c8cd224cf284e


Governance:


C4 BLOCKED · Publication BLOCKED · Lean OPEN · SDS-002 FROZEN/QUARANTINED · EK-001 QUARANTINED


Doctrine:


EXECUTION ≠ EVIDENCE ≠ PROOF


Frozen mathematical result


The adversarial continuation confirms the surviving transport identity:


[
m_T=0
\Longrightarrow
\Delta=\kappa_S
]


and the exact marked-support bound gives


[
0\le\kappa_S\le2.
]


Therefore


[
\boxed{
m_T=0
\Longrightarrow
0\le\Delta\le2
}
]


and, using


[
s_T=s_0+\Delta+m_T,
]


[
\boxed{
m_T=0
\Longrightarrow
s_T-s_0=\kappa_S\in{0,1,2}.
}
]


Consequently


[
\boxed{
m_T=0\Longrightarrow s_T\ge s_0.
}
]


The previous strengthening attempts are permanently rejected:


[
m_T=0\Rightarrow\Delta=0
]


is false,


[
m_T=0\Rightarrow\Delta\le1
]


is false, and


[
\kappa_S=2\Rightarrow m_T>0
]


is false.


The latter is now witnessed by the independently reconstructed n=14 fixture.


Independent reconstruction of the upper fixture


Take


[
X={0,\ldots,13},
\qquad T=(012).
]


Use


[
P=
{
{0,7,10},
{1,3,6},
{2,8,9},
{4,5,11,12,13}
}
]


and


[
Q=
{
{0,4,10},
{1,3},
{2,9},
{5,6},
{7,11},
{8,12,13}
}.
]


The independently reconstructed meet is


[
M=P\wedge Q


{
{0,10},
{1,3},
{2,9},
{4},
{5},
{6},
{7},
{8},
{11},
{12,13}
}
]


and


[
U=P\vee Q=X.
]


Thus


[
|P|=4,\qquad |Q|=6,\qquad |M|=10,\qquad |U|=1.
]


The correct slack is therefore


[
s_0=|M|+|U|-|P|-|Q|
=10+1-4-6
=1.
]


The raw expression


[
|P|+|Q|-|M|-|U|
]


is instead -1 and must never be used as s_0.


The closures independently reconstruct as


[
J_T(P)=
{
{0,1,2,3,6,7,8,9,10},
{4,5,11,12,13}
},
]


[
J_T(Q)=
{
{0,1,2,3,4,9,10},
{5,6},
{7,11},
{8,12,13}
},
]


[
J_T(M)=
{
{0,1,2,3,9,10},
{4},
{5},
{6},
{7},
{8},
{11},
{12,13}
},
]


and


[
J_T(U)=U.
]


Hence


[
|J_T(P)|=2,\quad
|J_T(Q)|=4,\quad
|J_T(M)|=8,\quad
|J_T(U)|=1.
]


The meet comparison gives


[
J_T(M)=J_T(P)\wedge J_T(Q),
]


so


[
m_T=0.
]


The closure losses are


[
(d_P,d_Q,d_M,d_U)


(2,2,2,0).
]


Therefore


[
\Delta


d_P+d_Q-d_M-d_U


2+2-2-0









]


The marked-block counts are


[
q_S(P)=3,\qquad
q_S(Q)=3,\qquad
q_S(M)=3,\qquad
q_S(U)=1,
]


so


[
\kappa_S=3+3-3-1=2.
]


Finally,


[
s_T


|J_T(M)|+|J_T(U)|
-|J_T(P)|-|J_T(Q)|
]


gives


[
s_T=8+1-2-4=3.
]


Thus the independently reconstructed fixture is


[
\boxed{
s_0=1,\quad
m_T=0,\quad
\kappa_S=2,\quad
\Delta=2,\quad
s_T=3.
}
]


This is a valid sharpness fixture.


The closure-loss lemma


Let


[
S={0,1,2}
]


and


[
q_S(R)


#{B\in R:B\cap S\neq\varnothing}.
]


Since T=(012) fixes every element outside S, the only blocks affected by


[
J_T(R)=R\vee T(R)\vee T^2(R)
]


are blocks meeting S.


Blocks disjoint from S remain unchanged. Therefore the reduction in the number of blocks is exactly the reduction in the number of marked blocks:


[
\boxed{
d_T(R)=|R|-|J_T(R)|


q_S(R)-q_S(J_T(R)).
}
]


This is the first substantive lemma.


Substitution into


[
\Delta=d_T(P)+d_T(Q)-d_T(M)-d_T(U)
]


gives


[
\Delta


\kappa_S(P,Q)


\kappa_S(J_T(P),J_T(Q))
]


provided the meet/join transport equalities are available.


The invariant marked-block lemma


If R is T-invariant, a block meeting S has only two possible forms.


Either all three marked points lie in one block:


[
S\subseteq B,
]


giving


[
q_S(R)=1,
]


or all three marked points are singleton blocks:


[
{0},{1},{2},
]


giving


[
q_S(R)=3.
]


There is no invariant configuration containing exactly two marked points in one block.


There is also no invariant configuration containing one marked point together with an outside point while keeping the other marked points separate: applying T would create overlapping translated blocks through the fixed outside point, forcing them to coincide and hence forcing all three marked points into one block.


For two invariant partitions, only four combinations remain:


[
(1,1),\quad(1,3),\quad(3,1),\quad(3,3).
]


Directly evaluating the marked meet/join counts in these four cases gives


[
\boxed{
R,W\text{ (T)-invariant}
\Longrightarrow
\kappa_S(R,W)=0.
}
]


This is the second substantive lemma.


The meet-transport lemma


Let


[
M=P\wedge Q.
]


Monotonicity of J_T gives


[
J_T(M)
\preceq
J_T(P)\wedge J_T(Q).
]


The meet defect is


[
m_T


r_{J_T(M)}


r_{J_T(P)\wedge J_T(Q)}.
]


If


[
m_T=0,
]


the two finite partitions have equal rank and one refines the other, hence they are equal:


[
\boxed{
m_T=0
\Longrightarrow
J_T(M)=J_T(P)\wedge J_T(Q).
}
]


The closure operator preserves joins:


[
\boxed{
J_T(P\vee Q)


J_T(P)\vee J_T(Q).
}
]


Consequently,


[
J_T(U)=J_T(P)\vee J_T(Q).
]


Under m_T=0,


[
\Delta


\kappa_S(P,Q)


\kappa_S(J_T(P),J_T(Q)).
]


Both J_T(P) and J_T(Q) are T-invariant, so the invariant marked-block lemma gives


[
\kappa_S(J_T(P),J_T(Q))=0.
]


Therefore


[
\boxed{
m_T=0
\Longrightarrow
\Delta=\kappa_S(P,Q).
}
]


This is the central transport theorem.


The marked-incidence bound


Construct the incidence graph from the three marked elements of S.


Each marked element supplies one incidence edge between its P-block and its Q-block.


Therefore


[
|E(H_S)|\le3.
]


The incidence graph is bipartite and simple. A nontrivial cycle in a simple bipartite graph requires at least four edges.


Hence


[
\beta(H_S)=0.
]


Using


[
\kappa_S


c(H_S)-c_G^{\mathrm{touched}}-\beta(H_S),
]


we obtain


[
\kappa_S


c(H_S)-c_G^{\mathrm{touched}}.
]


Since


[
1\le c_G^{\mathrm{touched}}
\le c(H_S)
\le3,
]


it follows that


[
\boxed{
0\le\kappa_S\le2.
}
]


Combining this with the transport theorem gives


[
\boxed{
m_T=0
\Longrightarrow
0\le\Delta=\kappa_S\le2.
}
]


The bound is therefore structurally local: it comes from the three-point support, not from a large finite census.


Exact transport interpretation


Under meet preservation,


[
m_T=0,
]


the transport increase is not merely bounded:


[
\boxed{
s_T-s_0=\kappa_S.
}
]


Thus the three possible transport levels are exactly


[
\kappa_S=0,\quad1,\quad2.
]


They correspond to


[
s_T-s_0=0,\quad1,\quad2.
]


The n=8 fixture realizes


[
\kappa_S=\Delta=1.
]


The n=14 fixture realizes


[
\kappa_S=\Delta=2.
]


Therefore the nonzero spectrum is experimentally realized at both levels.


Computational evidence


The following results remain supporting evidence rather than proof.


Local closure-loss classification through n=9:


[
\text{zero failures}.
]


Distinct m_T=0 pairs:


[
n=6:\quad 8{,}008\text{ cases},\qquad E=\Delta-\kappa_S=0
]


and


[
n=7:\quad 124{,}143\text{ cases},\qquad E=0.
]


The independently reconstructed n=8 fixture gives


[
(s_0,m_T,\kappa_S,\Delta,s_T)


(1,0,1,1,2).
]


The independently reconstructed n=14 fixture gives


[
(s_0,m_T,\kappa_S,\Delta,s_T)


(1,0,2,2,3).
]


No new exhaustive census is required to establish the mathematical target.


Frozen regression assertions


Every implementation must explicitly assert


[
r(R)=n-|R|,
]


[
s_0


r(P)+r(Q)-r(M)-r(U)


|M|+|U|-|P|-|Q|,
]


[
d_T(R)


r(J_T(R))-r(R)


|R|-|J_T(R)|,
]


[
s_T


r(J_T(P))+r(J_T(Q))
-r(J_T(M))-r(J_T(U)),
]


[
\Delta


d_P+d_Q-d_M-d_U,
]


[
m_T


r(J_T(M))
-r(J_T(P)\wedge J_T(Q)),
]


and


[
\boxed{
s_T=s_0+\Delta+m_T.
}
]


The sign convention is now a mandatory machine-level invariant.


Regression fixture N8


{
  "fixture": "C3-TRANSPORT-N8",
  "n": 8,
  "T": [0, 1, 2],
  "s0": 1,
  "mT": 0,
  "kappaS": 1,
  "d": [1, 1, 1, 0],
  "Delta": 1,
  "sT": 2,
  "E": 0,
  "status": "VERIFIED",
  "purpose": "rejects_Delta_zero"
}



Regression fixture N14


{
  "fixture": "C3-TRANSPORT-N14",
  "n": 14,
  "T": [0, 1, 2],
  "P": [
    [0, 7, 10],
    [1, 3, 6],
    [2, 8, 9],
    [4, 5, 11, 12, 13]
  ],
  "Q": [
    [0, 4, 10],
    [1, 3],
    [2, 9],
    [5, 6],
    [7, 11],
    [8, 12, 13]
  ],
  "M": [
    [0, 10],
    [1, 3],
    [2, 9],
    [4],
    [5],
    [6],
    [7],
    [8],
    [11],
    [12, 13]
  ],
  "U": [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
  ],
  "JP": [
    [0, 1, 2, 3, 6, 7, 8, 9, 10],
    [4, 5, 11, 12, 13]
  ],
  "JQ": [
    [0, 1, 2, 3, 4, 9, 10],
    [5, 6],
    [7, 11],
    [8, 12, 13]
  ],
  "JM": [
    [0, 1, 2, 3, 9, 10],
    [4],
    [5],
    [6],
    [7],
    [8],
    [11],
    [12, 13]
  ],
  "JU": [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
  ],
  "s0": 1,
  "mT": 0,
  "kappaS": 2,
  "d": [2, 2, 2, 0],
  "Delta": 2,
  "sT": 3,
  "E": 0,
  "status": "VERIFIED",
  "purpose": "rejects_Delta_le_one",
  "reconstruction": "independent_exact_partition_reconstruction"
}



The N14 full object should be committed as a new audit artifact. The currently linked public N14 JSON contains only the scalar summary, so it should not be described as a self-contained reconstruction certificate until the full arrays are added.


Formalization target


The Lean development should not begin with the entire historical C3 architecture.


The minimal dependency order is:


[
\text{partition lattice}
\rightarrow
J_T
\rightarrow
\text{closure loss}
]


[
\text{partition lattice}
\rightarrow
\text{marked invariant classification}
]


then


[
m_T=0
\rightarrow
J_T(M)=J_T(P)\wedge J_T(Q)
]


then


[
\Delta=\kappa_S
]


and finally


[
0\le\kappa_S\le2.
]


The first high-value theorem should be the transport identity:


transport_delta_eq_kappa



with the hypotheses made explicit rather than hidden in a large structure.


The graph lemma should remain separate.


Formal status


The mathematical argument is now reduced to a finite collection of explicit elementary lemmas.


However:


Lean definitions: OPEN


Lean compilation receipt: ABSENT


#print axioms receipt: ABSENT


zero-sorryAx audit: ABSENT


nanoda receipt: ABSENT


Lean SHA-256 certificate: ABSENT


Therefore the theorem must remain formally OPEN.


The phrase “mathematically proved” should be reserved in the frozen ledger for the handwritten mathematical derivation, while the formal-verification status remains OPEN.


Evidence status




Component
Status




Transport identity derivation
MATHEMATICALLY DERIVED


Upper bound 0\le\Delta\le2
MATHEMATICALLY DERIVED


N8 sharpness
VERIFIED FIXTURE


N14 sharpness
INDEPENDENTLY RECONSTRUCTED / VERIFIED


m_T=0\Rightarrow\Delta=\kappa_S
FORMALLY OPEN


Three-edge graph bound
FORMALLY OPEN


Sign convention
LOCKED / REGRESSION REQUIRED


Public N8 scalar JSON
PRESENT


Public N14 scalar JSON
PRESENT


Public N14 full reconstruction artifact
NOT YET PRESENT


Lean receipt
ABSENT


#print axioms
ABSENT


zero-sorry audit
ABSENT


EK-001
QUARANTINED


SDS-002
FROZEN / QUARANTINED


C4
BLOCKED


Publication
BLOCKED




Literature positioning


The invariant-partition literature supports the background statement that invariant partitions under a finite transitive permutation group form a sublattice. It does not establish the AQARION-specific identity


[
J_T(P\wedge Q)


J_T(P)\wedge J_T(Q)
]


for arbitrary P,Q. The latter remains a pair-specific meet-preservation condition represented here by m_T=0.


Partition-refinement literature supports the broader interpretation of partitions as computationally refined behavioral structures, but does not provide evidence for the transport theorem.


Recent Koopman-validation literature supports the methodological distinction between a computed finite-dimensional representation and a certified invariant structural object. It is contextual support only.


Provenance Run Crate supports the architectural separation of executions, intermediate outputs, and provenance records. It does not certify mathematical correctness.


None of these external sources changes the C3 mathematical status.


Frozen conclusion


The transport route survives.


The old numerical strengthening route does not.


The strongest supported statement is


[
\boxed{
m_T=0
\Longrightarrow
\Delta=\kappa_S
\in{0,1,2}.
}
]


Equivalently,


[
\boxed{
m_T=0
\Longrightarrow
s_T-s_0=\kappa_S.
}
]


The endpoint values are realized:


[
\boxed{\Delta=1\text{ at }n=8}
]


and


[
\boxed{\Delta=2\text{ at }n=14}.
]


The N14 witness is independently reconstructed and survives exact evaluation.


The next mathematical bottleneck is therefore no longer discovery of a bound. It is formal certification of:


[
d_T(R)=q_S(R)-q_S(J_T(R)),
]


[
T\text{-Invariant}(R,W)
\Rightarrow
\kappa_S(R,W)=0,
]


[
m_T=0
\Rightarrow
J_T(M)=J_T(P)\wedge J_T(Q),
]


followed by


[
\Delta=\kappa_S.
]


The graph bound


[
0\le\kappa_S\le2
]


should then be certified independently.


No C4.


No publication promotion.


No invented Lean receipt.


No resurrection of \Delta\le1.


No further search for an upper witness.


The only immediate artifact correction is to make the N14 public regression record self-contained by committing the complete partition arrays above.

https://huggingface.co/spaces/Quantarion9/AQARION-ACADEMY/resolve/main/CHECKPOINT.MD

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-CORE/JSON/AQ-S10-C3_TRANSPORT_N8.JSON/

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/AQARION-CORE/JSON/AQ-S10-C3-TRANSPORT.JSON/

https://huggingface.co/spaces/Quantarion9/AQARION-ACADEMY/blob/main/AQARION-CORE/DOCS/JSON/AQ-S10-C3_TRANSPORT_N8.JSON/

https://huggingface.co/spaces/Quantarion9/AQARION-ACADEMY/blob/main/AQARION-CORE/DOCS/JSON/AQ-S10-C3_TRANSPORT_N14.JSON/
