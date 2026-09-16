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
