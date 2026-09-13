#!/usr/bin/env bash
# init-research-workspace.sh
# Usage:
#   ./init-research-workspace.sh my-project
#   ./init-research-workspace.sh my-project --dir "$HOME/my-project"
#   ./init-research-workspace.sh my-project --no-git
#   ./init-research-workspace.sh my-project --force

set -euo pipefail

NAME=""
DIR=""
NO_GIT=0
FORCE=0

usage() {
  cat <<'EOF'
usage: init-research-workspace.sh <name> [--dir PATH] [--no-git] [--force]

Creates a conservative research workspace scaffold.

Options:
  --dir PATH   Destination directory. Default: ./<name>
  --no-git     Do not initialize a Git repository.
  --force      Permit use of an existing empty directory only.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)
      [[ $# -ge 2 ]] || { echo "error: --dir requires a path" >&2; exit 2; }
      DIR="$2"
      shift 2
      ;;
    --no-git)
      NO_GIT=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -z "$NAME" ]]; then
        NAME="$1"
      else
        echo "error: unexpected argument: $1" >&2
        usage >&2
        exit 2
      fi
      shift
      ;;
  esac
done

if [[ -z "$NAME" ]]; then
  usage >&2
  exit 2
fi

ROOT="${DIR:-./$NAME}"

if [[ -e "$ROOT" ]]; then
  if [[ ! -d "$ROOT" ]]; then
    echo "error: destination exists and is not a directory: $ROOT" >&2
    exit 1
  fi

  if [[ -n "$(find "$ROOT" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
    echo "error: destination exists and is non-empty: $ROOT" >&2
    echo "refusing to overwrite; choose another directory" >&2
    exit 1
  fi

  if [[ "$FORCE" -ne 1 ]]; then
    echo "error: destination exists: $ROOT" >&2
    echo "use --force only for an existing empty directory" >&2
    exit 1
  fi
fi

mkdir -p \
  "$ROOT/src" \
  "$ROOT/include" \
  "$ROOT/tests" \
  "$ROOT/apps" \
  "$ROOT/receipts" \
  "$ROOT/docs" \
  "$ROOT/scripts" \
  "$ROOT/data/raw" \
  "$ROOT/data/derived" \
  "$ROOT/fixtures" \
  "$ROOT/policies" \
  "$ROOT/schema" \
  "$ROOT/third_party" \
  "$ROOT/.claimlock"

cat > "$ROOT/README.md" <<'MD'
# Research Workspace

## Status

**EXPERIMENTAL.**

This workspace may contain numerical regression tests, specifications, and
reproducibility receipts. It does not imply:

- a Lean proof;
- a zero-sorry formal certificate;
- a publication-ready theorem;
- a hardware benchmark;
- a production security guarantee.

## Layout

- `src/` — implementation source
- `include/` — public headers
- `apps/` — command-line programs
- `tests/` — deterministic tests and negative controls
- `fixtures/` — versioned test inputs
- `docs/` — specification, conventions, limitations, reproducibility
- `scripts/` — deterministic local automation
- `receipts/` — generated execution evidence
- `schema/` — machine-readable output schemas
- `policies/` — policy definitions and fixtures
- `data/raw/` — immutable external or source inputs
- `data/derived/` — generated derived data

## Reproducibility

See `docs/REPRODUCIBILITY.md`.

A receipt is evidence for one declared source tree, command, environment, and
execution. It is not automatically a mathematical proof.
MD

cat > "$ROOT/.gitignore" <<'GI'
# Build products
build/
cmake-build-*/
CMakeFiles/
CMakeCache.txt
compile_commands.json
*.o
*.obj
*.a
*.lib
*.so
*.dylib
*.dll
*.exe

# Generated receipts and local logs
receipts/*
!receipts/.gitkeep
*.log
*.tmp

# Python and editor artifacts
__pycache__/
*.py[cod]
.venv/
.env
.DS_Store
.idea/
.vscode/

# Generated data
data/derived/*
!data/derived/.gitkeep
GI

touch "$ROOT/receipts/.gitkeep"
touch "$ROOT/data/derived/.gitkeep"

cat > "$ROOT/docs/REPRODUCIBILITY.md" <<'MD'
# Reproducibility

Every recorded run must preserve:

1. UTC timestamp.
2. Git commit ID, or explicit `UNVERSIONED` status.
3. `git status --porcelain` output.
4. SHA-256 hashes of relevant source, test, fixture, and specification files.
5. SHA-256 hash of the produced binary, if applicable.
6. Compiler version, CMake version, operating-system and architecture details.
7. Exact command line.
8. Full standard output and standard error.
9. Process exit status.
10. A machine-readable summary whose case counts are computed by the program.

Do not label a run as sealed merely because it says `PASS`.
MD

cat > "$ROOT/docs/THREAT_MODEL.md" <<'MD'
# Threat Model

This workspace tracks at least the following risks:

- A1: Scope laundering.
- A2: Stale result reuse.
- A4: Route-name duplication masking one implementation as two.
- A6: Hidden provenance cycles.
- A9: Canonicalization ambiguity.
- A11: Authority cycles.
- A13: Valid receipt paired with the wrong claim.
- A14: Authorized transition based on wrong evidence.
- A15: Impact overreach.
- CL001: Self-attested status.
- CL003: Hash identity ambiguity.

Mitigations require explicit specifications, negative controls, source hashes,
environment capture, and independent reproduction where appropriate.
MD

cat > "$ROOT/docs/LIMITATIONS.md" <<'MD'
# Limitations

Unless a versioned artifact explicitly states otherwise, this workspace does not
claim a formal Lean proof, a production RFC 8785 implementation, a hardware
benchmark, a physical-model interpretation, or a publication-ready result.

Numerical agreement, including exhaustive agreement over a finite parameter
range, is evidence for those tested cases only.
MD

cat > "$ROOT/scripts/capture-run.sh" <<'SH'
#!/usr/bin/env bash
# Usage:
#   ./scripts/capture-run.sh CLAIM_ID RUN_ID -- command arg1 arg2 ...

set -u -o pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: $0 CLAIM_ID RUN_ID -- command [args...]" >&2
  exit 2
fi

CLAIM_ID="$1"
RUN_ID="$2"
shift 2

if [[ "$1" != "--" ]]; then
  echo "error: expected -- before command" >&2
  exit 2
fi

shift

if [[ $# -eq 0 ]]; then
  echo "error: missing command" >&2
  exit 2
fi

CMD=( "$@" )
OUTDIR="receipts/$RUN_ID"

if [[ -e "$OUTDIR" ]]; then
  echo "error: receipt directory already exists: $OUTDIR" >&2
  exit 1
fi

mkdir -p "$OUTDIR"

{
  echo "receipt_schema=research.run-receipt.v1"
  echo "claim_id=$CLAIM_ID"
  echo "run_id=$RUN_ID"
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "[git_commit]"
  git rev-parse HEAD 2>&1 || echo "UNVERSIONED"
  echo
  echo "[git_status]"
  git status --porcelain 2>&1 || true
  echo
  echo "[platform]"
  uname -a 2>&1 || true
  echo
  echo "[compiler]"
  "${CXX:-c++}" --version 2>&1 || true
  echo
  echo "[cmake]"
  cmake --version 2>&1 || true
  echo
  echo "[source_sha256]"
  find src include apps tests docs fixtures scripts schema policies \
    -type f -print0 2>/dev/null \
    | sort -z \
    | xargs -0 -r sha256sum
  echo
  echo "[command]"
  printf '%q ' "${CMD[@]}"
  printf '
'
} > "$OUTDIR/meta.txt"

set +e
"${CMD[@]}" 2>&1 | tee "$OUTDIR/stdout.txt"
COMMAND_STATUS="${PIPESTATUS[0]}"
set -e

printf '%s
' "$COMMAND_STATUS" > "$OUTDIR/exit.txt"

if command -v sha256sum >/dev/null 2>&1; then
  find "$OUTDIR" -maxdepth 1 -type f -print0 \
    | sort -z \
    | xargs -0 sha256sum > "$OUTDIR/SHA256SUMS"
fi

echo "receipt_dir=$OUTDIR"
echo "command_exit_code=$COMMAND_STATUS"

exit "$COMMAND_STATUS"
SH

chmod +x "$ROOT/scripts/capture-run.sh"

if [[ "$NO_GIT" -eq 0 ]]; then
  git -C "$ROOT" init -q
  git -C "$ROOT" add -A

  if git -C "$ROOT" diff --cached --quiet; then
    echo "warning: nothing to commit" >&2
  elif git -C "$ROOT" commit -m "Initialize research workspace" >/dev/null 2>&1; then
    echo "git_initial_commit=created"
  else
    echo "warning: Git repository initialized but initial commit was not created." >&2
    echo "warning: configure user.name and user.email, then commit manually." >&2
  fi
fi

echo "initialized=$ROOT"
