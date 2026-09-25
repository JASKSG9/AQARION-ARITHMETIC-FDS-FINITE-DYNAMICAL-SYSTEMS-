MAIN-FILETREE.MD — AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS
Root: https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
Date: 2026-09-25 (observed from mobile GitHub screenshots)
Governance: C4 BLOCKED / PUBLICATION BLOCKED / PROMOTION FALSE
Purpose: Canonical root inventory, case-sensitive, as observed. No rename, no normalization.
This file is generated from observed repository state (screenshots 2026-09-25).
Entries marked with ...[TRUNCATED] were truncated by GitHub mobile UI.
Do not invent full names — resolve via git ls-tree -r --name-only HEAD on the real machine.
Exact Root Layout (case-sensitive)
Directories (12 + 5 nested-path entries)

.github/                          # last weekAI/                               # last weekAPI/                              # 2 months agoAPPS/                             # 2 months agoAQARION-CORE/                     # 2 weeks agoAQARION-LAKE/                     # last weekAQARION-SKILLS/                   # last weekARTIFACTS/                        # 3 months agoCHANGELOG/                        # last weekDATA/                             # 2 months agoDOCS/                             # 2 weeks agoLIBRARY/                          # 2 weeks agoMAIN-DIRECTORY/AQA...[TRUNCATED]  # 2 weeks ago — resolve full name via gitMAPS/                             # 2 months agoQUICKSTART/AQARIO...[TRUNCATED]   # last week — resolve full name via gitTESTS/                            # 2 weeks agoVERIFICATION/                     # last week
Files — Root Level (as listed, exact case)

.gitignore                        # 3 months agoAQ-SDS-001.PY                     # 2 weeks agoAQ-SDS-S9-001.JSON                # 2 weeks agoAQARION-ABSTRACT-0...[TRUNCATED]  # 2 months agoAQARION-AUDIT.HTML                # 2 weeks agoAQARION-DASHBOARD...[TRUNCATED]   # 3 months agoAQARION-QUICKSTART...[TRUNCATED]  # 2 months agoAQARION-RESEARCH-G...[TRUNCATED]  # 2 months agoAQARION.PY                        # 2 months agoAQARION_LEAN.YML                  # 3 weeks agoBIO-CONTACT.MD                    # 2 weeks agoCHECKPOINT.MD                     # 2 weeks agoCLAIMLOCK-DOD.MD                  # 2 weeks agoDEFECT.LEAN                       # 2 weeks agoGAP_THEOREM-MAP.MD                # 3 months agoKAPREKAR_KOOPMAN...[TRUNCATED]    # 3 months ago — first entryKAPREKAR_KOOPMAN...[TRUNCATED]    # 3 months ago — second entry, distinct file, resolve via gitKSG-AQARION-FDS-API...[TRUNCATED] # 3 months agoLICENSE                           # 2 weeks agoMAIN-DEMO.HTML                    # 3 weeks agoMAIN-FILETREE.MD                  # 2 weeks ago — THIS FILE (self-referential)OPEN_PROBLEMS.MD                  # 2 weeks agoPERMANENT-UPDATED...[TRUNCATED]   # 3 months agoPOLICY-LOCK.md                    # last week — note lower-case .mdPROOF-LEDGER.MD                   # 3 weeks agoREADME-LITE.MD                    # last weekREADME.MD                         # last weekSEPTEMBER-TESTS.MD                # 3 weeks agoUNDERVIEW.MD                      # 2 weeks ago
Canonical Tree (for copy-paste into repo)
text
.├── .github/├── AI/├── API/├── APPS/├── AQARION-CORE/├── AQARION-LAKE/├── AQARION-SKILLS/├── ARTIFACTS/├── CHANGELOG/├── DATA/├── DOCS/├── LIBRARY/├── MAIN-DIRECTORY/│   └── AQA...[TRUNCATED — resolve]├── MAPS/├── QUICKSTART/│   └── AQARIO...[TRUNCATED — resolve]├── TESTS/├── VERIFICATION/├── .gitignore├── AQ-SDS-001.PY├── AQ-SDS-S9-001.JSON├── AQARION-ABSTRACT-0...[TRUNCATED]├── AQARION-AUDIT.HTML├── AQARION-DASHBOARD...[TRUNCATED]├── AQARION-QUICKSTART...[TRUNCATED]├── AQARION-RESEARCH-G...[TRUNCATED]├── AQARION.PY├── AQARION_LEAN.YML├── BIO-CONTACT.MD├── CHECKPOINT.MD├── CLAIMLOCK-DOD.MD├── DEFECT.LEAN├── GAP_THEOREM-MAP.MD├── KAPREKAR_KOOPMAN...[TRUNCATED] (x2 — list both)├── KSG-AQARION-FDS-API...[TRUNCATED]├── LICENSE├── MAIN-DEMO.HTML├── MAIN-FILETREE.MD├── OPEN_PROBLEMS.MD├── PERMANENT-UPDATED...[TRUNCATED]├── POLICY-LOCK.md├── PROOF-LEDGER.MD├── README-LITE.MD├── README.MD├── SEPTEMBER-TESTS.MD└── UNDERVIEW.MD
How to Regenerate Authoritatively (run on real machine, Termux/Ubuntu)
Do NOT type from memory. Run these to get exact, non-truncated, case-sensitive list:
bash
# 1. repo identitygit rev-parse --show-toplevelgit branch --show-currentgit rev-parse HEAD
# 2. exact file listing, case-sensitive, no truncationgit ls-tree -r --name-only HEAD | sort > /tmp/full_tree.txtcat /tmp/full_tree.txt
# 3. top-level onlyls -1A --group-directories-first | sort
# 4. verify this file's hashsha256sum MAIN-FILETREE.MD
Then replace each [TRUNCATED] entry with the full path from full_tree.txt. Do not rename otherwise.
Status Notes
Observed live repo on 2026-09-25 contains 16 top-level dirs (including 2 nested-path dirs shown as folders in UI) and 29 root files.
POLICY-LOCK.md uses lower-case .md while most use upper .MD — preserve as is.
MAIN-FILETREE.MD already existed (2 weeks ago) — this version overwrites with observed inventory.
Skills surface is minimal (AQARION-SKILLS/ last week) — do not claim 12-skill catalogue as live.
Lean: DEFECT.LEAN present at root, AQARION_LEAN.YML present — not to be confused with Aqarion-Lean/ in other repo (Aqarion-Quantarion-AI).
Verification: VERIFICATION/ exists and was updated last week — aligns with adversarial checks.
Governance remains:

FROZEN AUDITC4: BLOCKEDPUBLICATION: BLOCKEDPROMOTION: FALSEEXTERNAL INDEPENDENT REPRODUCTION: NOT CLAIMED
Do not promote on filetree generation alone. Filetree is repository truth, not mathematical truth.
