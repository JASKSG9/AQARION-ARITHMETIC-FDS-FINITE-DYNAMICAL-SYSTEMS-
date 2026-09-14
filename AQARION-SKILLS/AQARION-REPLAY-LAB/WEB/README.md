
## `WEB/README.md`

This stops confusion about what belongs in the public-facing web folder.

```md
# WEB

This directory contains mobile/browser presentation files.

## Intended files

| File | Purpose |
|---|---|
| `index.html` | Main mobile landing page |
| `spectral-defect.html` | Live Float64 SV-001 numerical replay |
| `regression-museum.html` | Replayable rejected inference records |
| `replay-diff.html` | Side-by-side receipt comparison |
| `styles.css` | Shared visual style |

## Rules

- The web layer displays facts and receipts.
- The web layer does not assign stronger verdicts than the policy permits.
- Browser numeric output must be labeled `NUMERICALLY_MATCHED`.
- Browser output cannot be labeled `FORMALLY_PROVED`.
- Do not add arbitrary-code upload or execution controls.
- Do not display `SDS-002 CLEARED`, `C4 CLEARED`, or publication authorization unless those states are independently established.
