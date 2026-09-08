import json
import sys
from pathlib import Path

receipt_path = Path("Evidence/transport.json")
if not receipt_path.exists():
    receipt_path = Path(__file__).parent.parent / "Evidence" / "transport.json"
if not receipt_path.exists():
    receipt_path = Path("/mnt/data/AqarionLakeTest/Evidence/transport.json")

required = {
    "id",
    "title",
    "status",
    "source_scope",
    "claim",
    "schema_version"
}

try:
    with receipt_path.open(encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("AQARION RECEIPT INVALID")
    print(f"Missing receipt: {receipt_path}")
    sys.exit(1)
except json.JSONDecodeError as e:
    print("AQARION RECEIPT INVALID")
    print("Malformed JSON:", e)
    sys.exit(1)

missing = required - data.keys()
if missing:
    print("AQARION RECEIPT INVALID")
    print("Missing:", sorted(missing))
    sys.exit(1)

if data.get("status")!= "VERIFIED":
    print(f"AQARION RECEIPT INVALID: status={data.get('status')}!= VERIFIED")
    sys.exit(2)

print("AQARION RECEIPT VALID")
print(f"ID: {data['id']}")
print(f"Claim: {data['claim'][:80]}")
sys.exit(0)
