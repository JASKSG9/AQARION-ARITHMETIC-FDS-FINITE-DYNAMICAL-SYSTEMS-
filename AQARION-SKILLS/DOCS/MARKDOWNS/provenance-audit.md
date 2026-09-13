---
name: aqarion-provenance-audit
description: Detect session-echo and circular skill stubs in AQARION skill files by fingerprinting local workspace paths and prior command strings. Use when reviewing AQARION-SKILLS commits or before treating a skill file as upstream source. Cannot clear C4 or publication blocks.
---

# Provenance audit (adapter)

```bash
python3 aq/provenance_audit.py reports/github-AQ-S12-INIT.PY.snapshot reports/github-AQ-S12.SH.snapshot reports/github-AQ-S12.MD.snapshot
```

`SESSION_ECHO_SUSPECT` means do not treat the file as independent upstream evidence.
