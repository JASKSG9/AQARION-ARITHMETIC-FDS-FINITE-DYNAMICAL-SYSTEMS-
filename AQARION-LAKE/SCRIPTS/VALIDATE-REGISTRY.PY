#!/usr/bin/env python3

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "Evidence" / "transport.json"


def fail(message: str, code: int) -> None:
    print(f"AQARION RECEIPT INVALID - {message}")
    raise SystemExit(code)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if not RECEIPT.exists():
    fail("receipt missing", 2)

try:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
except Exception as exc:
    fail(f"invalid JSON: {exc}", 3)


required = {
    "id",
    "title",
    "status",
    "source_scope",
    "claim",
    "artifacts",
    "schema_version",
}

missing = sorted(required - data.keys())

if missing:
    fail(f"Missing: {missing}", 1)


if data["status"] != "VERIFIED":
    fail(f"status is {data['status']!r}, expected 'VERIFIED'", 4)


artifacts = data["artifacts"]

if not isinstance(artifacts, list) or not artifacts:
    fail("artifacts must be a non-empty array", 5)


for artifact in artifacts:
    required_artifact = {
        "kind",
        "name",
        "source",
        "source_sha256",
    }

    missing_artifact = sorted(
        required_artifact - artifact.keys()
    )

    if missing_artifact:
        fail(
            f"artifact missing fields: {missing_artifact}",
            6,
        )

    source = ROOT / artifact["source"]

    if not source.exists():
        fail(
            f"source file missing: {artifact['source']}",
            7,
        )

    expected_hash = artifact["source_sha256"]
    actual_hash = sha256_file(source)

    if expected_hash != actual_hash:
        print(
            "AQARION RECEIPT INVALID - SOURCE HASH MISMATCH"
        )
        print(f"  Expected: {expected_hash}")
        print(f"  Actual:   {actual_hash}")
        raise SystemExit(7)

    source_text = source.read_text(encoding="utf-8")

    declaration_name = artifact["name"].split(".")[-1]

    if declaration_name not in source_text:
        print(
            "AQARION ARTIFACT REFERENCE INVALID: "
            f"{artifact['name']} not in {artifact['source']}"
        )
        raise SystemExit(8)


print("AQARION RECEIPT VALID")
print(f"ID: {data['id']}")
print(f"Artifacts bound: {len(artifacts)}")
print("Source hash verified: "
      f"{artifacts[0]['source_sha256'][:20]}...")
