cat > engine/replayDiff.js <<'EOF'
export function replayDiff(left, right) {
  const paths = [
    "claim_contract.claim_id",
    "fixture.fixture_id",
    "execution.verifier_id",
    "facts.tested_cases",
    "facts.extremizer_count",
    "policy_evaluation.verdict"
  ];

  const get = (object, path) => {
    return path
      .split(".")
      .reduce((value, key) => value == null ? undefined : value[key], object);
  };

  const comparison = {};
  const blocking_differences = [];

  for (const path of paths) {
    const a = get(left, path);
    const b = get(right, path);

    if (a === undefined || b === undefined) {
      comparison[path] = "MISSING";
    } else if (JSON.stringify(a) === JSON.stringify(b)) {
      comparison[path] = "MATCH";
    } else {
      comparison[path] = "MISMATCH";
    }

    if (comparison[path] !== "MATCH") {
      blocking_differences.push({
        field: path,
        left: a ?? null,
        right: b ?? null
      });
    }
  }

  const countSwap =
    get(left, "facts.tested_cases") !== undefined &&
    get(right, "facts.extremizer_count") !== undefined;

  return {
    schema_version: "aqarion.replay-diff.v0.1",
    left_receipt: left.receipt_id ?? "LEFT",
    right_receipt: right.receipt_id ?? "RIGHT",
    comparison,
    semantic_result: countSwap
      ? "COUNT_SEMANTIC_FAIL"
      : (blocking_differences.length ? "SEMANTIC_MISMATCH" : "MATCH"),
    blocking_differences
  };
}
EOF
