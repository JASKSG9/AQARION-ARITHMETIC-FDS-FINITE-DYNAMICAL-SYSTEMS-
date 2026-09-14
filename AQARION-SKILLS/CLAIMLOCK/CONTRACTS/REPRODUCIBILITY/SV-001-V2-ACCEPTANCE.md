SV-001-V2 Acceptance Contract


Status: FROZEN


1. Scope


This contract governs deterministic verification of:


G = U^T D^T D U


for:


D = (I-P)K_sP


under the finite domain:


2 <= m <= 8
2 <= k <= 8
1 <= s < mk


with:


n = mk


and equal contiguous blocks of size k.


2. Operator Convention


The Koopman/permutation matrix is:


K[x,(x+s) mod n] = 1.


The block projection is the orthogonal averaging projection onto vectors constant on each contiguous block.


U is the normalized block-indicator isometry satisfying:


P = UU^T
U^T U = I.


3. Target Identity


Let:


r = s mod k


and:


alpha_sq = r(k-r)/k^2.


Then:


G = alpha_sq(2I-S-S^T).


For m=2, S=S^T and the target is the doubled-edge form.


4. Operator Norm Target


If m is even:


||D||_2 = 2 sqrt(alpha_sq).


If m is odd:


||D||_2


2 sqrt(alpha_sq)
cos(pi/(2m)).


5. Exact Domain Case Count


The declared domain contains:


1176


cases.


This value must be independently derived from the domain by any receipt checker.


It must not be trusted merely because it appears as a constant.


6. Acceptance Conditions


A runtime result is PASS only if:




every domain case executes;


cases_executed equals the independently derived domain count;


zero-r and nonzero-r branches partition the executed cases;


no non-finite values occur;


maximum Gram error is <= 1e-12;


maximum norm error is <= 1e-12;


all failure counters are zero.




7. Prohibited Evidence


The following do not establish this contract:




hardcoded displayed errors;


manually copied totals;


a successful process that exits nonzero;


an unread receipt;


a receipt parsed by an undocumented lossy mechanism;


an AI agent statement that the verifier passed.




8. Meta-Verification


The runtime receipt must itself be checked for internal consistency by an independent receipt verifier.


9. Promotion


SV-001-V2 runtime PASS does not by itself promote:




C4;


publication status;


Lean status;


any theorem beyond the contract scope.




Promotion remains a separate policy decision.
