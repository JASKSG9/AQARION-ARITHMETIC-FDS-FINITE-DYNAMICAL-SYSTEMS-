
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

# Root output directory
ROOT = Path("/mnt/agents/output/AQARION")

# Create full directory tree
dirs = [
    "verification/tests",
    "verification/counterexamples",
    "verification/reference_data",
    "verification/reports",
    "claims",
    "docs",
    "lean",
    "src/aqarion",
    "benchmarks",
    ".github/workflows"
]

for d in dirs:
    (ROOT / d).mkdir(parents=True, exist_ok=True)

print("Directory tree created:")
for d in sorted(dirs):
    print(f"  {d}/")
