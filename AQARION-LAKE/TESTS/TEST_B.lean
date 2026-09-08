import Lake
open Lake DSL

package AqarionLakeTestB where
  version := v!"0.1.0"

input_file evidenceJsonFile where
  path := "Evidence/transport.json"
  text := true

input_file coreSourceFile where
  path := "AqarionLake/Core.lean"
  text := true

@[default_target]
target validateEvidence pkg : Unit := do
  let _ ← evidenceJsonFile.fetch
  let _ ← coreSourceFile.fetch
  let result ← IO.Process.output {
    cmd := "python3"
    args := #["scripts/validate_registry.py"]
  }
  if result.exitCode!= 0 then
    IO.eprint result.stdout
    IO.eprint result.stderr
    throw <| IO.userError s!"AQARION evidence validation failed (code {result.exitCode})"
  IO.println result.stdout
  let evidenceDir := pkg.buildDir / "evidence"
  IO.FS.createDirAll evidenceDir
  let src := pkg.dir / "Evidence" / "transport.json"
  let dst := evidenceDir / "registry.receipt.json"
  IO.FS.writeFile dst (← IO.FS.readFile src)

@[default_target]
lean_lib AqarionLake where
  roots := #[`AqarionLake]
  needs := #[validateEvidence]

@[default_target]
lean_exe aqarionLakeTest where
  root := `Main
  needs := #[validateEvidence]
