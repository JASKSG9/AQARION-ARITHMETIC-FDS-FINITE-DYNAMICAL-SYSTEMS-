"""RPL-001: failure must still produce complete receipt."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "scripts" / "capture.py"


def test_success_receipt(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir()
    (tmp_path / "RECEIPTS").mkdir()
    cmd = [
        sys.executable,
        str(CAPTURE),
        "AQ-OK",
        "RPL-OK",
        "--",
        sys.executable,
        "-c",
        "print(42)",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    data = json.loads((tmp_path / "runs" / "RPL-OK" / "receipt.json").read_text())
    assert data["exit_code"] == 0
    assert data["verdict"] == "COMPUTED"
    assert data["promotion_allowed"] is False


def test_failure_still_writes_receipt(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "runs").mkdir()
    (tmp_path / "RECEIPTS").mkdir()
    cmd = [
        sys.executable,
        str(CAPTURE),
        "AQ-FAIL",
        "RPL-FAIL",
        "--",
        sys.executable,
        "-c",
        "import sys; print('boom'); sys.exit(7)",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 7, (r.returncode, r.stderr)
    path = tmp_path / "runs" / "RPL-FAIL" / "receipt.json"
    assert path.exists(), "RPL-001 VIOLATION: missing failure receipt"
    data = json.loads(path.read_text())
    assert data["exit_code"] == 7
    assert data["verdict"] == "FAILED"
    assert data["residual"] is not None
    assert data["promotion_allowed"] is False
    assert (tmp_path / "RECEIPTS" / "AQ-RPL-RPL-FAIL.json").exists()
