import json
import sys
import hashlib
from pathlib import Path

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

repo_root = Path(__file__).parent.parent
receipt_path = repo_root / "Evidence" / "transport.json"
if not receipt_path.exists():
    receipt_path = Path("/mnt/data/AqarionLakeTestB/Evidence/transport.json")

with open(receipt_path) as f:
    data = json.load(f)

required_top = {"id","claim","artifacts","schema_version"}
missing_top = required_top - data.keys()
if missing_top:
    print("AQARION RECEIPT INVALID - missing top keys:", sorted(missing_top))
    sys.exit(1)

claim = data.get("claim", {})
required_claim = {"id","title","status","source_scope"}
missing_claim = required_claim - claim.keys()
if missing_claim:
    print("AQARION RECEIPT INVALID - missing claim fields:", sorted(missing_claim))
    sys.exit(2)

if claim.get("status")!= "VERIFIED":
    print(f"AQARION RECEIPT INVALID: status={claim.get('status')}")
    sys.exit(3)

integrity = data.get("integrity", {})
stored_hash = integrity.get("receipt_hash")
if stored_hash:
    import copy
    tmp = copy.deepcopy(data)
    tmp.get("integrity", {}).pop("receipt_hash", None)
    calc = hashlib.sha256(json.dumps(tmp, sort_keys=True).encode()).hexdigest()
    if calc!= stored_hash:
        print("AQARION RECEIPT INVALID - RECEIPT HASH MISMATCH")
        print(f" Stored: {stored_hash[:16]}...")
        print(f" Calc: {calc[:16]}...")
        sys.exit(9)

artifacts = data.get("artifacts", [])
if not artifacts:
    print("AQARION RECEIPT INVALID - no artifacts")
    sys.exit(4)

for art in artifacts:
    src = art.get("source")
    expected_hash = art.get("source_sha256")
    name = art.get("name")
    if not src or not expected_hash:
        print(f"AQARION RECEIPT INVALID - artifact {name} missing source/hash")
        sys.exit(5)
    src_path = repo_root / src
    if not src_path.exists():
        src_path = Path("/mnt/data/AqarionLakeTestB") / src
    if not src_path.exists():
        print(f"AQARION ARTIFACT REFERENCE INVALID: {src} not found")
        sys.exit(6)
    actual_hash = sha256_file(src_path)
    if actual_hash!= expected_hash:
        print("AQARION RECEIPT INVALID - SOURCE HASH MISMATCH")
        print(f" Artifact: {name}")
        print(f" Expected: {expected_hash}")
        print(f" Actual: {actual_hash}")
        sys.exit(7)
    if name.split(".")[-1] not in src_path.read_text():
        print(f"AQARION ARTIFACT REFERENCE INVALID: {name} not in {src}")
        sys.exit(8)

print("AQARION RECEIPT VALID")
print(f"ID: {data.get('id')}")
print(f"Artifacts bound: {len(artifacts)}")
print(f"Source hash verified: {artifacts[0]['source_sha256'][:16]}...")
sys.exit(0)
