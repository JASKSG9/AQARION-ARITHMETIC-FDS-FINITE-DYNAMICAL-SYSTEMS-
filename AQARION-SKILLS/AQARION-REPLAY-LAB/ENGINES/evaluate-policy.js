cat > engine/evaluatePolicy.js <<'EOF'
export const VERDICTS = Object.freeze({
  FORMALLY_PROVED: "FORMALLY_PROVED",
  EXACTLY_VERIFIED: "EXACTLY_VERIFIED",
  NUMERICALLY_MATCHED: "NUMERICALLY_MATCHED",
  EMPIRICALLY_SUPPORTED: "EMPIRICALLY_SUPPORTED",
  REFUTED: "REFUTED",
  OPEN: "OPEN",
  INADMISSIBLE: "INADMISSIBLE",
  BLOCKED: "BLOCKED"
});

export function evaluateSemanticFirewall({
  contract,
  facts,
  requestedVerdict
}) {
  if (!contract || !facts) {
    return {
      verdict: VERDICTS.INADMISSIBLE,
      rule: "MALFORMED_RECORD"
    };
  }

  if (
    contract.governance?.publication_allowed === false &&
    requestedVerdict === VERDICTS.FORMALLY_PROVED
  ) {
    return {
      verdict: VERDICTS.BLOCKED,
      rule: "GOVERNANCE_BLOCK"
    };
  }

  if (facts.carrierMatch === false) {
    return {
      verdict: VERDICTS.INADMISSIBLE,
      rule: "CARRIER_MISALIGNMENT"
    };
  }

  if (
    facts.domainComplete === false &&
    requestedVerdict === VERDICTS.EXACTLY_VERIFIED
  ) {
    return {
      verdict: VERDICTS.INADMISSIBLE,
      rule: "DOMAIN_VIOLATION"
    };
  }

  if (
    facts.numericOnly === true &&
    requestedVerdict === VERDICTS.FORMALLY_PROVED
  ) {
    return {
      verdict: VERDICTS.INADMISSIBLE,
      rule: "EVIDENCE_PROMOTION_FAIL"
    };
  }

  if (facts.operatorMismatch === true) {
    return {
      verdict: VERDICTS.INADMISSIBLE,
      rule: "SEMANTIC_OPERATOR_MISMATCH"
    };
  }

  if (facts.invarianceIdentityConfusion === true) {
    return {
      verdict: VERDICTS.INADMISSIBLE,
      rule: "INVARIANCE_IDENTITY_CONFUSION"
    };
  }

  return {
    verdict: requestedVerdict,
    rule: "ALLOW"
  };
}
EOF
