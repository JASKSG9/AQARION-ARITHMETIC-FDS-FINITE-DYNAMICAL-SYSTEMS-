# Clone the self‑contained repository
git clone https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-

# Install exact dependencies
pip install -r verification/requirements.txt

# Run full verification (tests + Lean + evidence hashes)
make verify

# Generate all derived artifacts (papers, RO‑Crate, dashboard)
make generate

# View the live Research Graph
make dashboard
