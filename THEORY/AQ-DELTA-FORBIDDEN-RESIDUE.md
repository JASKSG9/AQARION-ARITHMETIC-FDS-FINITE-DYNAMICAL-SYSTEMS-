AQ-DELTA-FORBIDDEN-RESIDUE-001


2026-09-27


Status


CLOSED — analytic theorem with independent computational verification.


Evidence:




[T] analytic


[C2] exhaustive finite verification


Scope: 3\le k\le16,\ 1\le d<k


119 parameter pairs


119/119 agreement




The historical formula


[
\delta(k,d)=\frac{k}{\gcd(k,d)}
]


is KILLED.


It fails on 114 of the 119 tested pairs.


Correct persistence formula


Let T(i)=i+1\pmod{k}, and let


[
R(k,d)
]


denote the forbidden residue set for persistence of the pair partition
{{0,d}}.


Then


[
\boxed{
\delta(k,d)


\min{m\ge1:m\bmod k\notin R(k,d)}.
}
]


This is the persistence index.


It is distinct from the subgroup closure quantity


[
|\langle d\rangle|


\frac{k}{\gcd(k,d)}.
]


Computational verification


For all


[
3\le k\le16,\qquad1\le d<k,
]


there are 119 parameter pairs.


The independent rerun gives:




\delta
count




1
66


2
47


3
4


4
2




The distribution agrees exactly with the canonical artifact.


Separation of invariants


Three quantities must not be conflated:


[
\gcd(k,d)
]


is the number of blocks in the cyclic closure,


[
\frac{k}{\gcd(k,d)}
]


is the subgroup order,


and


[
\delta(k,d)
]


is the persistence index.


They answer different questions.


Governance


The old gcd-ratio formula remains permanently KILLED.


No computational enumeration is being promoted as the proof of the formula; the computation is retained as independent verification of the analytic result.


