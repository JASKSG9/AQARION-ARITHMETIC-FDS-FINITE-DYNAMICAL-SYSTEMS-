import pathlib
root=pathlib.Path("AQARION-LAKE")
assert (root/"lakefile.lean").exists(), "lakefile missing"
assert (root/"AqarionLake.lean").exists(), "ONE ROOT missing"
assert (root/"lean-toolchain").exists()
print("PRESENT+WIRED=PASS")
print("lake build should now compile AqarionLake")
