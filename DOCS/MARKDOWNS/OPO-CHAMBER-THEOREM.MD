# OP0_CHAMBER_THEOREM.md — Closed-Form Chamber Inequalities

**Status:** `[CV]`, exhaustively verified over the full 54-state domain `G`
(see PROOFS.md §OP0b for exact epistemic status — this is a verified
computational fact, with a partial symbolic explanation (§OP0a in
PROOFS.md), not yet a complete first-principles proof).

## The result

Every chamber of the AQARION 4-digit gap quotient is **exactly** the
intersection of `G = {0≤g2≤g1≤9}\{(0,0)}` with a small system of linear
inequalities in `g1`, `g2`, `g1+g2`, `g1-g2` — a genuine combinatorial
"why," not merely an enumerated list.

| # | Inequality system (minimal, verified) | Size | Branch matrix `M` | `t` | `det` |
|---|---|---|---|---|---|
| 1 | `g2≥5  ∧  g1-g2≥1` | 10 | `[[2,0],[0,2]]` | `(-10,-10)` | `+4` |
| 2 | `9≤g1+g2≤10  ∧  1≤g1-g2≤8` | 8 | `[[1,-1],[1,-1]]` | `(1,-1)` | `0` |
| 3 | `g1≤4  ∧  g2≥1  ∧  g1-g2≥1` | 6 | `[[0,-2],[-2,0]]` | `(10,10)` | `-4` |
| 4 | `g1≥5  ∧  g2≥1  ∧  g1+g2≤8` | 6 | `[[0,-2],[2,0]]` | `(10,-10)` | `+4` |
| 5 | `g2≤4  ∧  g1+g2≥11` | 6 | `[[2,0],[0,-2]]` | `(-10,10)` | `-4` |
| 6 | `g2=0  ∧  g1-g2≤5` | 5 | `[[-1,0],[1,0]]` | `(10,-1)` | `0` |
| 7 | `g1+g2≤8  ∧  g1-g2=0` | 4 | `[[-1,-1],[-1,-1]]` | `(11,9)` | `0` |
| 8 | `g2=0  ∧  g1-g2≥6` | 4 | `[[1,0],[-1,0]]` | `(-1,10)` | `0` |
| 9 | `g1+g2≥12  ∧  g1-g2=0` | 4 | `[[1,1],[1,1]]` | `(-9,-11)` | `0` |
| 10 | `g1+g2=10  ∧  g1-g2=0` | 1 | — (singleton, image `(1,1)`) | — | — |

`Σ size = 10+8+6+6+6+5+4+4+4+1 = 54` ✓ matches `|G|` exactly.
`{det} = {-4, 0, +4}` ✓ matches the checkpoint's claimed set exactly.
Every matrix entry lies in `{-2,-1,0,1,2}` — the dynamics never amplify a
gap coordinate by more than a factor of 2 per step within a chamber.

## Reading the table geometrically

- **Chambers 1, 3, 4, 5** (the four `det=±4` chambers) are the **rank-2**
  branches — invertible local maps, scaling each gap coordinate by exactly
  `±2`. These sit in the "interior" diagonal bands of the simplex.
- **Chambers 2, 6, 7, 8, 9** (`det=0`) are **rank-1** — they collapse a full
  line of states onto a single output value. Notably **6, 8** are the two
  halves of the `g2=0` edge (split at `g1-g2=5` ⟷ `g1=5`, exactly OP0a's
  borrow/no-borrow boundary in PROOFS.md), and **7, 9** are the two halves
  of the main diagonal `g1=g2` (split at `g1=5`).
- **Chamber 10** is the single point `(5,5)` — the simplex's natural center,
  sitting exactly on both split boundaries above, mapping to `(1,1)` (inside
  chamber 7).
- The unique fixed point `(6,2)` ↔ Kaprekar's constant `6174` sits inside
  chamber 4 (`det=+4`, an expanding-then-contracting branch in disguise —
  it is a fixed point of `T_G` overall even though `M` has det `+4`, because
  `(6,2)` solves `M·v+t=v` exactly: `[[0,-2],[2,0]]·(6,2)+(10,-10) = (0-4+10,
  12-10) = (6,2)` ✓).

## Visual

See `chamber_heatmap.png`: left panel = chamber id per `(g1,g2)`, right panel
= `det(M_k)` per state. The fixed point `(6,2)` is ringed in the left panel.

## What remains open

1. **Symbolic derivation for chambers 2–5, 7, 9** (analogous to OP0a's clean
   borrow argument for 6/8): each boundary above (`g1+g2=10/11`, `g1-g2`
   thresholds) should correspond to a specific carry/borrow event in the
   subtraction `999g1+90g2`'s digit decomposition. OP0a derived this fully
   for the `g2=0` axis; the general case needs the same treatment applied to
   `r=90g2-g1`'s hundreds/tens decomposition. This is mechanical but not yet
   carried out here.
2. **Generalization.** Does an analogous *bounded-functional* (small,
   fixed-size inequality system) characterization hold for `d`-digit
   Kaprekar in base `b` generally, or is `d=4,b=10`'s clean 4-functional
   description special? Untested — flagged as the natural Phase I/II
   benchmark-expansion question from CHECKPOINT.md.
3. Whether 4 linear functionals (`g1,g2,sum,diff`) are *provably* always
   sufficient (vs. occasionally needing a 5th, e.g. `2g1-g2`) for *any*
   piecewise-affine quotient map of this general shape is not established;
   it was sufficient here, verified, not derived as a structural necessity.
