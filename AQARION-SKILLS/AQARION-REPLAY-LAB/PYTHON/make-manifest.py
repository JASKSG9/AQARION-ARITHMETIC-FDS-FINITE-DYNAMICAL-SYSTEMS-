cat > make_manifest.py <<'EOF'
import hashlib
import json
from pathlib import Path

ROOT = Path(".")
SKIP = {
    ".git",
    "__pycache__",
    "receipts"
}

files = []

for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue

    if any(part in SKIP for part in path.parts):
        continue

    data = path.read_bytes()

    files.append({
        "path": str(path),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest()
    })

manifest = {
    "artifact": "aqarion-replay-lab",
    "version": "0.1.0-draft",
    "kind": "development-manifest",
    "limitations": [
        "Not RFC 8785 canonicalized",
        "Not signed",
        "Not a Sigstore/Rekor attestation",
        "Not a formal proof receipt",
        "Not a publication authorization"
    ],
    "files": files
}

Path("MANIFEST.json").write_text(
    json.dumps(manifest, indent=2) + "
",
    encoding="utf-8"
)

print(f"Wrote MANIFEST.json with {len(files)} files.")
EOF

python3 make_manifest.py
