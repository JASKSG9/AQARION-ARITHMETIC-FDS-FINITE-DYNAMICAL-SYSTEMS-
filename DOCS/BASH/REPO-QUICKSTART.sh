#!/bin/bash
# REPO-QUICKSTART.sh
# Zero‑to‑research in one command

set -e

echo "🚀 AQARION Quickstart"
echo "====================="

# 1. Clone if not already in the repo
if [ ! -d "AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-" ]; then
    echo "📦 Cloning repository..."
    git clone https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
    cd AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
else
    cd AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
fi

# 2. Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r verification/requirements.txt

# 3. Run verification
echo "🧪 Running verification..."
./DOCS/BASH/VERIFIED-QUICKSTART-RUN-ALL.sh

# 4. Generate derived artifacts (if generation scripts exist)
echo "📄 Generating artifacts..."
if [ -f "governance/generate_artifacts.py" ]; then
    python3 governance/generate_artifacts.py
else
    echo "⚠️  Artifact generation script not found – skipping."
fi

# 5. Launch dashboard (optional)
if [ "$1" == "--dashboard" ]; then
    echo "🌐 Launching dashboard..."
    if [ -f "interactive/dashboard.py" ]; then
        python3 interactive/dashboard.py &
        sleep 2
        echo "   Dashboard running at http://localhost:5000"
    else
        echo "⚠️  Dashboard not found – skipping."
    fi
fi

echo ""
echo "✅ AQARION is ready."
echo "   - Papers: papers/"
echo "   - RO-Crate: ro-crate/"
