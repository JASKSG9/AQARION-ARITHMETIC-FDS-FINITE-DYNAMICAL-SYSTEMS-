
# ============================================================
# 10. AQARION-FLOW.md — Development & Release Workflow
# ============================================================

flow_doc = """# AQARION v0.4.1-final — Development & Release Workflow

## The AQARION Development Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLAIM     │────>│  EVIDENCE   │────>│ CERTIFICATE │
│   DEFINED   │     │  COMPUTED   │     │  GENERATED  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │  VERIFIER   │
                                         │  INDEPENDENT│
                                         └──────┬──────┘
                                                │
                              ┌─────────────────┼─────────────────┐
                              │                 │                 │
                              ▼                 ▼                 ▼
                        ┌─────────┐      ┌─────────┐       ┌─────────┐
                        │  VALID  │      │ INVALID │       │  ERROR  │
                        │ (green) │      │  (red)  │       │ (gray)  │
                        └────┬────┘      └────┬────┘       └────┬────┘
                             │                │                 │
                             ▼                ▼                 ▼
                        ┌─────────┐      ┌─────────┐       ┌─────────┐
                        │ ARCHIVE │      │  DEBUG  │       │  DEBUG  │
                        │ RELEASE │      │  & FIX  │       │  & FIX  │
                        └─────────┘      └─────────┘       └─────────┘
```

## Release Checklist (v0.4.1-final)

### Pre-Release

- [ ] All tests pass (`python -m unittest test_aqarion -v`)
- [ ] All certificates generated with `status: UNVERIFIED`
- [ ] All certificates independently verified as `VALID`
- [ ] Registry version frozen (`REGISTRY_VERSION = "0.4.1-final"`)
- [ ] Schema version locked (`certificate_version = "3.1.0"`)
- [ ] All file versions consistent (`0.4.1-final`)
- [ ] Hash manifest generated (`SHA256SUM`)
- [ ] Docker builds successfully
- [ ] README.md updated
- [ ] CHANGELOG.md updated

### Release Steps

1. **Freeze Registry**
   ```python
   REGISTRY_VERSION = "0.4.1-final"  # No changes after this
   ```

2. **Generate Certificates**
   ```bash
   python main.py generate AQ-CLAIM-001
   python main.py generate AQ-CLAIM-002
   python main.py generate AQ-CLAIM-003
   python main.py generate AQ-CLAIM-004
   ```

3. **Verify All Certificates**
   ```bash
   python verify_certificate.py AQ-CERT-AQ-CLAIM-001-001.json
   python verify_certificate.py AQ-CERT-AQ-CLAIM-002-001.json
   python verify_certificate.py AQ-CERT-AQ-CLAIM-003-001.json
   python verify_certificate.py AQ-CERT-AQ-CLAIM-004-001.json
   ```

4. **Generate Hash Manifest**
   ```bash
   sha256sum aqarion_kernel.py verify_certificate.py main.py test_aqarion.py \
             Dockerfile requirements.txt README.md \
             AQ-CERT-*.json registry_snapshot.json system_definition.json \
             VERIFY_OUTPUT.txt VERSION.txt > SHA256SUM
   ```

5. **Build Docker Image**
   ```bash
   docker build -t aqarion:0.4.1-final .
   docker run aqarion:0.4.1-final
   ```

6. **Tag Release**
   ```bash
   git tag -a v0.4.1-final -m "AQARION v0.4.1-final — Reference Artifact Ready"
   git push origin v0.4.1-final
   ```

7. **Publish Reference Artifact**
   ```bash
   # Create reference artifact directory
   mkdir -p AQARION-REFERENCE-ARTIFACT/certificates
   cp AQ-CERT-*.json AQARION-REFERENCE-ARTIFACT/certificates/
   cp SHA256SUM VERIFY_OUTPUT.txt registry_snapshot.json \
      system_definition.json VERSION.txt README.md \
      AQARION-REFERENCE-ARTIFACT/
   
   # Upload to GitHub releases
   # Upload to Zenodo for DOI
   # Upload to HuggingFace datasets
   ```

## Post-Release

- [ ] Announce on GitHub Discussions
- [ ] Update Replit deployment
- [ ] Update HuggingFace README
- [ ] Begin v0.5.0 development branch

## Version Numbering

```
v{major}.{minor}.{patch}-{stage}

major: Breaking changes to certificate schema
minor: New features, new claims, new theorems
patch: Bug fixes, documentation updates
stage: alpha, beta, rc (release candidate), final

Examples:
  v0.4.1-final   — Frozen reference artifact
  v0.5.0-alpha   — Development branch
  v1.0.0-rc1     — Release candidate
```

## Git Branching Model

```
main        ─────●─────●─────●─────●─────●─────●───>
                 │     │     │     │     │     │
                 │     │     │     │     │     └── v0.5.0-alpha
                 │     │     │     │     └── v0.4.2
                 │     │     │     └── v0.4.1-final  ← YOU ARE HERE
                 │     │     └── v0.4.1-rc2
                 │     └── v0.4.1-rc1
                 └── v0.4.0-final
```

## Claim Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   DRAFT     │────>│  REGISTERED │────>│  CERTIFIED  │
│   (idea)    │     │  (in code)  │     │  (generated)│
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │  VERIFIED   │
                                         │  (community)│
                                         └─────────────┘
```

## Emergency Procedures

### Certificate Compromise

1. Do NOT regenerate with same claim ID
2. Create new claim ID (e.g., AQ-CLAIM-001-v2)
3. Update registry
4. Generate new certificate
5. Publish advisory

### Registry Version Mismatch

```
Error: Registry version mismatch
Certificate: 0.4.0-final
Current: 0.4.1-final
```

**Resolution:** Regenerate certificate with current kernel.

### Hash Integrity Failure

```
Error: Hash integrity check failed
```

**Resolution:** Certificate was modified. Regenerate or restore from backup.
"""

with open(os.path.join(output_dir, "AQARION-FLOW.md"), 'w') as f:
    f.write(flow_doc)

print("✅ AQARION-FLOW.md")
