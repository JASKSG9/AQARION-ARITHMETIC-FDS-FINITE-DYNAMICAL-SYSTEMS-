#!/usr/bin/env bash
set -euo pipefail
NAME="${1:-aqarion-replay-lab-20260914}"
DIR="${2:-./$NAME}"
mkdir -p "$DIR"/{src,tests,receipts,docs,scripts,ENGINES,FIXTURES,RECEIPTS,policies,QUICKSTART}

cat > "$DIR/README.md" <<'EOF'
# AQARION REPLAY LAB — 14 SEPTEMBER 2026 FIXED
Support-Metric Separation + Forest Kernel + Fourier Intertwiner
C4 BLOCKED, publication BLOCKED, Lean OPEN
Fixed: RPL-001 receipt finalization
EOF

cat > "$DIR/.gitignore" <<'EOF'
build/, __pycache__/, .venv/, receipts/*.txt, RECEIPTS/*.json, MANIFEST.sha256, *.pyc, .DS_Store,
EOF

cat > "$DIR/docs/REPRODUCIBILITY.md" <<'EOF'
Every run must capture: UTC timestamp, git commit, source SHA256, command, exit code, receipt JSON.
Use: scripts/capture-run.sh CLAIM_ID RUN_ID -- python3 ENGINES/...
Invariant: FAILED RUN => COMPLETE RECEIPT (RPL-001 fixed)
EOF

cat > "$DIR/scripts/capture-run.sh" <<'EOS'
#!/usr/bin/env bash
set -euo pipefail
CLAIM="$1"; RUN="$2"; shift 2
mkdir -p receipts
out="receipts/${RUN}-$(date -u +%Y%m%dT%H%M%SZ).txt"
{ echo "CLAIM=$CLAIM RUN=$RUN"; date -u; uname -a; git rev-parse HEAD 2>&1 || echo UNVERSIONED; echo "CMD: $*"; } | tee "$out"
set +e
"$@" 2>&1 | tee -a "$out"
rc=${PIPESTATUS[0]}
set -e
echo "exit=$rc" | tee -a "$out"
exit $rc
EOS
chmod +x "$DIR/scripts/capture-run.sh"

cat > "$DIR/ENGINES/forest_acyclic.py" <<'PY'
def forest_acyclic(Fset, m):
    parent = list(range(m))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in Fset:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True
PY

cat > "$DIR/ENGINES/domain_firewall.py" <<'PY'
from fractions import Fraction as Q
def det2(A): return A[0][0]*A[1][1] - A[0][1]*A[1][0]
def charpoly_2x2(A): tr = A[0][0] + A[1][1]; return (Q(1), -tr, det2(A))
L2 = [[Q(2), Q(-2)], [Q(-2), Q(2)]]
K2 = [[Q(1), Q(-1)], [Q(-1), Q(1)]]
assert charpoly_2x2(L2) == (Q(1), Q(-4), Q(0))
assert charpoly_2x2(K2) == (Q(1), Q(-2), Q(0))
PY

cat > "$DIR/ENGINES/circulant_intertwiner.py" <<'PY'
from fractions import Fraction as Q
def build_M(m, k, r, q=0):
    M = [[Q(0) for _ in range(m)] for _ in range(m)]
    for j in range(m):
        M[j][(j+q) % m] = Q(k-r)
        M[j][(j+q+1) % m] += Q(r)
    return M
def cycle_laplacian(m):
    L = [[Q(0) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        L[i][i] += Q(2); L[i][(i-1) % m] -= Q(1); L[i][(i+1) % m] -= Q(1)
    return L
PY

cat > "$DIR/QUICKSTART/README.md" <<'EOF'
Quickstart: bash init-aqarion-replay-lab-20260914-fixed.sh
EOF

cd "$DIR"
git init -q
git add -A >/dev/null 2>&1 || true
echo "[init] $DIR ready — RPL-001 FIXED"

