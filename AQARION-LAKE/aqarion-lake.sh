cd AQARION-LAKE

# 1. Fix case
git mv LAKEFILE.lean lakefile.lean
git mv TOOLCHAIN.lean lean-toolchain
git mv MAIN.lean Main.lean
git mv CORE.lean Core.lean
git mv VALIDATE-REGISTRY.py validate_registry.py
git mv EVIDENCE-TRANSPORT.json transport.json
rm TRANSPORT.json REGISTRY.py ELAN-BASH.sh LAKE-EXPERIMENT-001.MD

# 2. Create correct layout
mkdir -p AqarionLake Evidence scripts TESTS
git mv Core.lean AqarionLake/Core.lean
git mv transport.json Evidence/transport.json
git mv validate_registry.py scripts/validate_registry.py

# 3. Overwrite with frozen contents we proved
cat > lakefile.lean << 'EOF'
import Lake
open Lake DSL

package AqarionLakeTest where
  version := v!"0.1.0"

input_file transportEvidence where
  path := "Evidence/transport.json"
  text := true

@[default_target]
target validateEvidence pkg : Unit := do
  let _ ← transportEvidence.fetch
  let result ← IO.Process.output {
    cmd := "python3"
    args := #["scripts/validate_registry.py"]
  }
  if result.exitCode!= 0 then
    IO.eprint result.stdout
    IO.eprint result.stderr
    throw <| IO.userError "AQARION evidence validation failed"
  IO.println result.stdout
  let evidenceDir := pkg.buildDir / "evidence"
  IO.FS.createDirAll evidenceDir
  IO.FS.writeFile (evidenceDir / "registry.receipt.json") (← IO.FS.readFile (pkg.dir / "Evidence" / "transport.json"))

@[default_target]
lean_lib AqarionLake where
  roots := #[`AqarionLake]
  needs := #[validateEvidence]

@[default_target]
lean_exe aqarionLakeTest where
  root := `Main
  needs := #[validateEvidence]
EOF

echo "leanprover/lean4:v4.21.0" > lean-toolchain

cat > Main.lean << 'EOF'
import AqarionLake.Core
def main : IO Unit := IO.println "AQARION LAKE EXPERIMENT 001 BUILD SUCCEEDED"
EOF

# 4. Commit
git add -A
git commit -m "EXP-001: lowercase Lake layout, public-API lakefile, frozen receipt"
git push
