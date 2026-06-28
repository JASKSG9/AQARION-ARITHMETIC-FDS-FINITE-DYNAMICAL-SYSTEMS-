# Generate GitHub Actions workflow
ci_yaml = '''name: AQARION Verification Suite

on:
  push:
    branches: [main, master, develop]
  pull_request:
    branches: [main, master]
  release:
    types: [created, published]
  workflow_dispatch:
    inputs:
      tier:
        description: 'Maximum verification tier to run'
        required: true
        default: '5'
        type: choice
        options:
          - '1'
          - '2'
          - '3'
          - '4'
          - '5'

jobs:
  # ============================================================
  # TIER 1: Structural Integrity (Always runs, fast)
  # ============================================================
  tier-1-gate:
    name: Tier 1 — Gate Checks
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install minimal dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Verify repository structure
        run: |
          cd verification
          python verify_repository.py --repo-root .. --evidence-dir ../evidence

      - name: Verify artifact hashes
        run: |
          cd verification
          python verify_hashes.py --repo-root .. --evidence-dir ../evidence

      - name: Upload evidence artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: tier-1-evidence
          path: evidence/
          retention-days: 30

  # ============================================================
  # TIER 2: Core Mathematics (Runs if Tier 1 passes)
  # ============================================================
  tier-2-mathematics:
    name: Tier 2 — Core Mathematics
    needs: tier-1-gate
    if: success()
    runs-on: ubuntu-latest
    timeout-minutes: 30
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install numpy scipy sympy networkx matplotlib
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Verify projection operators
        run: |
          cd verification
          python verify_projection.py --repo-root .. --evidence-dir ../evidence

      - name: Verify Koopman operators
        run: |
          cd verification
          python verify_koopman.py --repo-root .. --evidence-dir ../evidence

      - name: Verify graph invariants
        run: |
          cd verification
          python verify_graph.py --repo-root .. --evidence-dir ../evidence
          python verify_scc.py --repo-root .. --evidence-dir ../evidence
          python verify_cycles.py --repo-root .. --evidence-dir ../evidence

      - name: Verify Kaprekar benchmarks
        run: |
          cd verification
          python verify_kaprekar.py --repo-root .. --evidence-dir ../evidence

      - name: Upload evidence artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: tier-2-evidence-py${{ matrix.python-version }}
          path: evidence/
          retention-days: 30

  # ============================================================
  # TIER 3: Deep Audit (Runs on schedule or manual trigger)
  # ============================================================
  tier-3-deep:
    name: Tier 3 — Deep Audit
    needs: tier-2-mathematics
    if: github.event_name == 'schedule' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    timeout-minutes: 60
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install numpy scipy sympy networkx matplotlib
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run counterexample census
        run: |
          cd verification
          python verify_counterexamples.py --repo-root .. --evidence-dir ../evidence

      - name: Run random FDD validation
        run: |
          cd verification
          python verify_random_fdds.py --repo-root .. --evidence-dir ../evidence

      - name: Run census generation
        run: |
          cd verification
          python verify_census.py --repo-root .. --evidence-dir ../evidence

      - name: Upload evidence artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: tier-3-evidence
          path: evidence/
          retention-days: 30

  # ============================================================
  # TIER 4: Formal & Publication (Runs on release or manual)
  # ============================================================
  tier-4-formal:
    name: Tier 4 — Formal & Publication
    needs: tier-2-mathematics
    if: github.event_name == 'release' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Verify Lean build (if Lean present)
        run: |
          if [ -f lakefile.lean ]; then
            cd verification
            python verify_lean.py --repo-root .. --evidence-dir ../evidence
            python verify_no_sorry.py --repo-root .. --evidence-dir ../evidence
          else
            echo "No Lean formalization detected — skipping Lean checks"
          fi

      - name: Verify paper artifacts
        run: |
          cd verification
          python verify_figures.py --repo-root .. --evidence-dir ../evidence
          python verify_tables.py --repo-root .. --evidence-dir ../evidence
          python verify_papers.py --repo-root .. --evidence-dir ../evidence

      - name: Upload evidence artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: tier-4-evidence
          path: evidence/
          retention-days: 30

  # ============================================================
  # TIER 5: Release Gate (Runs only on release creation)
  # ============================================================
  tier-5-release:
    name: Tier 5 — Release Gate
    needs: [tier-2-mathematics, tier-4-formal]
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Verify release metadata
        run: |
          cd verification
          python verify_release.py --repo-root .. --evidence-dir ../evidence

      - name: Verify CI configuration
        run: |
          cd verification
          python verify_ci.py --repo-root .. --evidence-dir ../evidence

      - name: Run master referee (full suite)
        run: |
          cd verification
          python referee.py --tier 5 --output-dir ../reports

      - name: Upload final reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: release-reports
          path: |
            reports/
            evidence/
          retention-days: 90

  # ============================================================
  # LINT: Enforce verifier independence
  # ============================================================
  lint-verifier-independence:
    name: Lint — Verifier Independence
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Check for banned imports in verifiers
        run: |
          BANNED=("from aqarion" "import aqarion" "from src." "import src_")
          VIOLATIONS=0
          for file in verification/*.py; do
            for pattern in "${BANNED[@]}"; do
              if grep -q "$pattern" "$file"; then
                echo "VIOLATION: $file contains banned pattern: $pattern"
                VIOLATIONS=$((VIOLATIONS + 1))
              fi
            done
          done
          if [ $VIOLATIONS -gt 0 ]; then
            echo "Found $VIOLATIONS verifier independence violations"
            exit 1
          fi
          echo "No verifier independence violations found"

  # ============================================================
  # REPRODUCIBILITY: Fresh clone test
  # ============================================================
  reproducibility:
    name: Reproducibility — Fresh Clone
    needs: tier-1-gate
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run reproducibility verification
        run: |
          cd verification
          python verify_reproducibility.py --repo-root .. --evidence-dir ../evidence --skip-clone

      - name: Upload evidence
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: reproducibility-evidence
          path: evidence/
          retention-days: 30
'''

with open("/mnt/agents/output/aqarion_audit.yml", 'w') as f:
    f.write(ci_yaml)

print("[SAVED] aqarion_audit.yml (GitHub Actions workflow)")[SAVED] aqarion_audit.yml (GitHub Actions workflow)
