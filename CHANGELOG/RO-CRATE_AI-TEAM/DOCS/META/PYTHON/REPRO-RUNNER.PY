import subprocess, pathlib, json, sys
FIXED_TIMESTAMP = "2026-07-16T00:00:00+00:00"
BASE = pathlib.Path(__file__).parent.parent
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, cwd=str(BASE), capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr
def main():
    print("[AQTC-005] Reproducibility runner - 3x clean verification")
    hashes = []
    for i in range(1,4):
        print(f"  Run {i}/3...")
        rc, out, err = run_cmd(f"{sys.executable} -m src.registry_loader")
        if rc != 0:
            print(f"    FAIL registry loader: {err} {out}")
            return False
        rc, out, err = run_cmd(f"{sys.executable} -m src.dependency_graph")
        if rc != 0:
            print(f"    FAIL graph generator: {err} {out}")
            return False
        rc, out, err = run_cmd(f"{sys.executable} -m src.manifest")
        if rc != 0:
            print(f"    FAIL manifest: {err} {out}")
            return False
        with open(BASE / "certificates/manifest.sha256.json") as f:
            data = json.load(f)
        hashes.append(data["manifest_hash"])
    reproducible = hashes[0]==hashes[1]==hashes[2]
    print(f"  Hashes: {hashes}")
    print(f"  Reproducible: {reproducible}")
    report = {
        "test_id": "AQTC-005",
        "runs": 3,
        "hashes": hashes,
        "reproducible": reproducible,
        "timestamp": FIXED_TIMESTAMP,
        "status": "pass" if reproducible else "fail"
    }
    with open(BASE / "reports/aqtc-005-reproducibility.json", 'w') as f:
        json.dump(report, f, sort_keys=True, indent=2)
    print(f"[AQTC-005] {'PASS' if reproducible else 'FAIL'}")
    return reproducible
if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)

