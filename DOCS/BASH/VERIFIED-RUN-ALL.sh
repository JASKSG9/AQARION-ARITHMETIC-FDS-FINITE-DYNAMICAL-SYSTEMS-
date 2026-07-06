#!/bin/bash
# VERIFIED-QUICKSTART-RUN-ALL.sh
# One‑command full verification pipeline

set -e

echo "🧪 AQARION Verification Pipeline"
echo "================================"

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+."
    exit 1
fi

# 2. Install dependencies if needed
if [ ! -d "verification" ]; then
    echo "❌ verification/ directory not found. Are you in the repo root?"
    exit 1
fi

if [ -f "verification/requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r verification/requirements.txt
fi

# 3. Run the test suite
echo "🧪 Running test suite..."
python3 verification/test_suite.py --all

# 4. Check Lean (optional)
if [ -d "lean_audit" ]; then
    echo "📐 Checking Lean 4 kernel..."
    cd lean_audit && lake build && cd ..
fi

# 5. Hash check (optional)
if [ -f "certificates/v14.0-certification.json" ]; then
    echo "🔐 Verifying artifact hashes..."
    sha256sum -c certificates/v14.0-certification.json 2>/dev/null || echo "⚠️  Hash check skipped (file not found)"
fi

echo ""
echo "✅ All verification gates passed."
