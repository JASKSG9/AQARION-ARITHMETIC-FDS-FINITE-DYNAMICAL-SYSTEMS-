import Lake
open Lake DSL

package aqarionLake where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.34.0-rc1"

@[default_target]
lean_lib AqarionLake where
  roots := #[`AqarionLake]

lean_exe aqarionLakeTest where
  root := `Main
