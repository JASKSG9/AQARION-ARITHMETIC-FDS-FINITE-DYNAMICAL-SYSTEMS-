#!/usr/bin/env python3
"""
AQARION SV-001 receipt meta-verifier.

Checks consistency between:
- declared domain,
- executed case count,
- branch counts,
- failure counts,
- finite numeric values,
- status.

This verifier is intentionally independent of the
matrix construction implementation.
"""

import argparse
import json
import math
import sys


REQUIRED_SCHEMA = (
    "aqarion.sv001.verifier-result.v2"
)


def expected_case_count(domain: dict) -> int:
    total = 0

    for m in range(
        domain["m_min"],
        domain["m_max"] + 1,
    ):
        for k in range(
            domain["k_min"],
            domain["k_max"] + 1,
        ):
            total += m * k - 1

    return total


def finite_number(value) -> bool:
    return (
        isinstance(value, (int, float))
        and math.isfinite(float(value))
    )


def validate_receipt(receipt: dict) -> list[str]:
    errors = []

    if (
        receipt.get("receipt_schema")
        != REQUIRED_SCHEMA
    ):
        errors.append(
            "receipt_schema mismatch"
        )

    if "domain" not in receipt:
        errors.append(
            "missing domain"
        )
        return errors

    if "result" not in receipt:
        errors.append(
            "missing result"
        )
        return errors

    domain = receipt["domain"]
    result = receipt["result"]

    try:
        expected = expected_case_count(
            domain
        )
    except Exception as exc:
        errors.append(
            f"invalid domain: {exc}"
        )
        return errors

    if (
        result.get("cases_executed")
        != expected
    ):
        errors.append(
            "cases_executed does not match domain"
        )

    zero_cases = result.get(
        "zero_r_cases"
    )

    nonzero_cases = result.get(
        "nonzero_r_cases"
    )

    if (
        zero_cases is None
        or nonzero_cases is None
    ):
        errors.append(
            "missing r branch counts"
        )
    elif (
        zero_cases + nonzero_cases
        != result.get("cases_executed")
    ):
        errors.append(
            "r branch counts do not partition total"
        )

    for key in (
        "max_gram_error",
        "max_norm_error",
    ):
        if not finite_number(
            result.get(key)
        ):
            errors.append(
                f"{key} is not finite"
            )

    failures = (
        result.get(
            "gram_failures",
            -1,
        )
        + result.get(
            "norm_failures",
            -1,
        )
        + result.get(
            "nonfinite_failures",
            -1,
        )
    )

    expected_status = (
        "PASS"
        if (
            failures == 0
            and result.get(
                "cases_executed"
            )
            == expected
            and (
                zero_cases is not None
                and nonzero_cases is not None
                and zero_cases + nonzero_cases
                == expected
            )
        )
        else "FAIL"
    )

    if (
        result.get("status")
        != expected_status
    ):
        errors.append(
            "status does not match evidence"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "receipt",
        type=str,
    )

    args = parser.parse_args()

    try:
        with open(
            args.receipt,
            "r",
            encoding="utf-8",
        ) as handle:
            receipt = json.load(handle)

    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "FAIL",
                    "errors": [
                        f"receipt load failure: {exc}"
                    ],
                },
                indent=2,
            )
        )
        return 1

    errors = validate_receipt(
        receipt
    )

    output = {
        "schema": (
            "aqarion.sv001.receipt-check.v1"
        ),
        "status": (
            "PASS"
            if not errors
            else "FAIL"
        ),
        "errors": errors,
    }

    print(
        json.dumps(
            output,
            indent=2,
            allow_nan=False,
        )
    )

    return (
        0
        if not errors
        else 1
    )


if __name__ == "__main__":
    sys.exit(main())
