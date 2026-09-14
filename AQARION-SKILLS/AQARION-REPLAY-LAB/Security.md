
## 4. SECURITY.md

```sh
cat > SECURITY.md <<'EOF'
# Security Policy

AQARION Replay Lab v0.1 is a research prototype.

## Do not submit

- private keys
- API tokens
- credentials
- private datasets
- untrusted code
- binaries
- shell scripts intended for execution
- production signing material

## Scope

The first release supports curated repository fixtures only.

It does not safely sandbox arbitrary uploaded code.

It does not provide production-grade receipt signing, immutable provenance, RFC 8785 canonicalization, Sigstore/Rekor inclusion, or authorization guarantees.

## Reporting

Report suspected issues involving:

- semantic-policy bypass;
- domain inflation;
- verdict promotion;
- receipt mismatch;
- schema-validation bypass;
- dependency-integrity failure;
- incorrect regression fixture behavior.

Do not claim that development SHA-256 hashes provide production provenance.
EOF
