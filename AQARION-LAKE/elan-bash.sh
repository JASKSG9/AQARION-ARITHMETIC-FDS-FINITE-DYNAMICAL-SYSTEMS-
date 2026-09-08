lake update
python3 scripts/validate_registry.py
lake build
test -f.lake/build/evidence/registry.receipt.json
# negative
python3 -c "import json; d=json.load(open('Evidence/transport.json')); del d['source_scope']; json.dump(d, open('Evidence/transport.json','w'))"
lake build; echo $?
# expected non-zero
