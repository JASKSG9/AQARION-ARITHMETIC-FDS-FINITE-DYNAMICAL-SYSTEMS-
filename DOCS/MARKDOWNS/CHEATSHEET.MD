# CHEATSHEET.md — AQARION Gap-Quotient System, One Screen

```
K(n) = desc(n) - asc(n)                         4-digit Kaprekar map
n -> sort digits desc: a>=b>=c>=d                D2
pi(n) = (g1,g2) = (a-d, b-c)                     gap projection

EXACT IDENTITY (no piecewise correction needed at this step):
    K(n) = 999*g1 + 90*g2                        [P+CV] T1

STATE SPACE:  G = {0<=g2<=g1<=9} \ {(0,0)}        |G| = 54           [CV]

QUOTIENT MAP: T_G(g1,g2) = pi(999*g1 + 90*g2)     well-defined, closed on G

FIXED POINT:  (6,2)  <->  6174  (Kaprekar's constant)   UNIQUE, no other cycles
MAX DEPTH:    D = 6   =   nu(N)   (Nilpotency-Depth Lemma, L1)
SPECTRUM:     sigma(P_G) = {0, 1}
FILTRATION:   54 -> 20 -> 14 -> 10 -> 7 -> 4 -> 1
```

## The 10 chambers (ASCII map of the (g1,g2) simplex)

```
g2
 9  . . . . . . . . . 9
 8  . . . . . . . . 9 1
 7  . . . . . . . 9 1 1
 6  . . . . . . 9 1 1 1
 5  . . . . .10 1 1 1 1
 4  . . . . 7 2 2 5 5 5
 3  . . . 7 3 4 2 2 5 5
 2  . . 7 3 3 4 4 2 2 5
 1  . 7 3 3 3 4 4 4 2 2
 0  . 6 6 6 6 6 8 8 8 8
    0 1 2 3 4 5 6 7 8 9   g1
```
(digit = chamber id; `.` = outside `G`, i.e. `g2>g1` or the excluded `(0,0)`)

## det(M_k) by chamber

```
chamber:  1   2   3   4   5   6   7   8   9   10
det(M_k): +4   0  -4  +4  -4   0   0   0   0   —(singleton)
rank:      2   1   2   2   2   1   1   1   1    —
```

## Evidence label legend

```
[P]        proved here, direct algebra
[CV]       exhaustively verified by computation (entire finite domain)
[P+CV]     both
[O]        open
[undefined] term used in CHECKPOINT.md without a definitions file yet
```

## New results this session (none previously claimed)

```
OP0a   [P]    g2=0 axis splits via thousands-digit borrow, at g1=5/6
OP0b   [CV]   every chamber = box in {g1, g2, g1+g2, g1-g2}, exact, all 10
T12-suff [P]  f constant-on-fibers => [id,~] = product of fiber lattices
T12-ce  [P+CV-toy]  fiber-respecting but non-constant f can break the product
T12-app [P]   AQARION's own pi is constant-on-fibers (by T1) => T12 holds here
```

## Files in this package

```
README.md                  start here
DEFINITIONS.md              D1-D16, incl. flagged [PROPOSED] FNDS objects
CLAIMS_REGISTER.md          single source of truth, every claim -> label
PROOFS.md                   T0-T4, L1, OP0a, OP0b, T12-suff/ce/app
OP0_CHAMBER_THEOREM.md       full inequality table + geometric reading
AUDIT_REPORT.md              checkpoint claim <-> reproduction, line by line
DEPENDENCY_GRAPH.mmd         mermaid, paste into mermaid.live or GitHub .md
chamber_heatmap.png          chamber id + det(M_k), visual
verify.py / verify_report.json / .sha256   the actual reproducible engine
```
