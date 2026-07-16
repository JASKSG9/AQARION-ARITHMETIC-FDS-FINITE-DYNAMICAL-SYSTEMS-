
# Debug: why do AQTC-002 and aq_verify fail from reproduce.py but pass when run directly?
# The issue is likely that reproduce.py runs from ROOT but the tests also cd to ROOT,
# and there might be a path resolution issue.

# Let's check what happens when we run them directly

print("=== Direct AQTC-002 ===")
result = subprocess.run(
    [sys.executable, str(ROOT / "tests" / "test_registry_loader.py")],
    capture_output=True, text=True, cwd=str(ROOT)
)
print("stdout:", result.stdout[:500])
print("stderr:", result.stderr[:500] if result.stderr else "None")
print("exit:", result.returncode)

print("\n=== Direct aq_verify ===")
result2 = subprocess.run(
    [sys.executable, str(ROOT / "aq_verify.py"), str(ROOT / "certificates" / "TEST-001_certificate.json")],
    capture_output=True, text=True, cwd=str(ROOT)
)
print("stdout:", result2.stdout[:500])
print("stderr:", result2.stderr[:500] if result2.stderr else "None")
print("exit:", result2.returncode)=== Direct AQTC-002 ===
stdout: ============================================================
AQTC-002 TEST: Claim Registry Loader
============================================================

stderr: Traceback (most recent call last):
  File "/mnt/agents/output/AQARION-TOOL-CHAIN/tests/test_registry_loader.py", line 112, in <module>
    main()
  File "/mnt/agents/output/AQARION-TOOL-CHAIN/tests/test_registry_loader.py", line 91, in main
    test_all_claims_load()
  File "/mnt/agents/output/AQARION-TOOL-CHAIN/tests/test_registry_loader.py", line 42, in test_all_claims_load
    assert report["claims_loaded"] == 3, "Expected 3 claims, got " + str(report["claims_loaded"])
           ^^^^^^^^^^^^
exit: 1

=== Direct aq_verify ===
stdout: {
  "claim_id": "TEST-001",
  "errors": [
    "Manifest hash mismatch: stored=4c989f3b68097dad83cfeff0cd26bfdba663278f36789ece6bd886aff7ca1e9f recomputed=0b10408f6e30e3066cba01c8a408279b9498f12482be2c2651c1d10f73db2583"
  ],
  "manifest_artifacts": 35,
  "recomputed_certificate_hash": "56035516505af3bb6299b2b86e79eb62177871f3227603550e89c7683c5a07e2",
  "recomputed_manifest_hash": "0b10408f6e30e3066cba01c8a408279b9498f12482be2c2651c1d10f73db2583",
  "record_id": "CERT-TEST-001-20260716",
  "stat
stderr: None
exit: 1
