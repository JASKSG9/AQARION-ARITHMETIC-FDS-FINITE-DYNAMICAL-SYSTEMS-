import Lake
open Lake DSL
package AqarionLakeTest where version := v!"0.1.0"
input_file transportEvidence where path := "Evidence/transport.json"; text := true
@[default_target]
target validateEvidence pkg : Unit := do
  let _ ← transportEvidence.fetch
  let result ← IO.Process.output { cmd := "python3", args := #["scripts/validate_registry.py"] }
  if result.exitCode!= 0 then throw <| IO.userError "AQARION evidence validation failed"
  let evidenceDir := pkg.buildDir / "evidence"
  IO.FS.createDirAll evidenceDir
  IO.FS.writeFile (evidenceDir / "registry.receipt.json") (← IO.FS.readFile (pkg.dir / "Evidence" / "transport.json"))
@[default_target]
lean_lib AqarionLake where roots := #[`AqarionLake]; needs := #[validateEvidence]
@[default_target]
lean_exe aqarionLakeTest where root := `Main; needs := #[validateEvidence]
