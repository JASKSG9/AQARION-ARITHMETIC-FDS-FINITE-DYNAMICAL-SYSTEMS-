#!/usr/bin/env python3
"""
AQARION adversarial verifier for SV-001-V2.

This file does not certify SV-001.

It certifies that the SV-001 reference checker is capable
of detecting selected classes of structural error.
"""

import json
import math
import sys

import numpy as np

from sv001_v2_check import (
    ABS_TOL,
    alpha_sq_from_shift,
    build_cycle_laplacian,
    evaluate_case,
    evaluate_sv001,
)


SUITE = "AQ-ML-ADVERSARY-002"


def check(name: str, condition: bool, detail: str) -> dict:
    return {
        "name": name,
        "passed": bool(condition),
        "detail": detail,
    }


def test_r_zero() -> dict:
    result = evaluate_case(
        m=4,
        k=4,
        s=4,
    )

    return check(
        "r_zero_exact_boundary",
        result["r"] == 0
        and result["gram_error"] <= ABS_TOL
        and result["norm_error"] <= ABS_TOL,
        "r=0 must yield exact zero defect target.",
    )


def test_m_two_boundary() -> dict:
    L = build_cycle_laplacian(2)

    expected = np.array(
        [
            [2.0, -2.0],
            [-2.0, 2.0],
        ],
        dtype=np.float64,
    )

    return check(
        "m_two_double_edge_laplacian",
        np.array_equal(L, expected),
        "m=2 must realize 2I-2S.",
    )


def test_large_wrap() -> dict:
    alpha_sq = alpha_sq_from_shift(
        k=4,
        s=11,
    )

    return check(
        "multi_period_shift_wrap",
        abs(alpha_sq - 3.0 / 16.0)
        <= 1.0e-15,
        "s=11 mod 4=3 gives alpha_sq=3/16.",
    )


def test_actual_case_execution() -> dict:
    result = evaluate_case(
        m=5,
        k=4,
        s=11,
    )

    return check(
        "reference_case_executes",
        result["finite"]
        and result["gram_error"] <= ABS_TOL
        and result["norm_error"] <= ABS_TOL,
        "Reference verifier must pass a wrapped shift.",
    )


def test_wrong_alpha_is_detectable() -> dict:
    m = 5
    k = 4
    s = 11

    alpha_sq_correct = alpha_sq_from_shift(k, s)

    alpha_sq_wrong = (
        (s % k) / float(k)
    )

    L = build_cycle_laplacian(m)

    correct_target = (
        alpha_sq_correct * L
    )

    wrong_target = (
        alpha_sq_wrong * L
    )

    detectable = (
        np.max(
            np.abs(
                correct_target
                - wrong_target
            )
        )
        > ABS_TOL
    )

    return check(
        "wrong_alpha_negative_control",
        detectable,
        "Deliberately wrong alpha formula must differ.",
    )


def test_wrong_laplacian_is_detectable() -> dict:
    m = 5

    L = build_cycle_laplacian(m)

    S = np.zeros(
        (m, m),
        dtype=np.float64,
    )

    for i in range(m):
        S[i, (i + 1) % m] = 1.0

    wrong_L = (
        np.eye(m)
        - S
    )

    detectable = (
        np.max(
            np.abs(L - wrong_L)
        )
        > ABS_TOL
    )

    return check(
        "wrong_laplacian_negative_control",
        detectable,
        "One-sided shift target must differ from cycle Laplacian.",
    )


def test_reference_receipt_consistency() -> dict:
    receipt = evaluate_sv001()

    result = receipt["result"]
    consistency = receipt["consistency"]

    ok = (
        consistency[
            "case_count_matches_domain"
        ]
        and consistency[
            "r_partition_matches_total"
        ]
        and result["status"] == "PASS"
        and result["cases_executed"]
        == consistency[
            "expected_cases_from_domain"
        ]
    )

    return check(
        "receipt_internal_consistency",
        ok,
        "Receipt counts and status must agree.",
    )


def test_nan_rejected_by_json_policy() -> dict:
    hostile = {
        "x": float("nan"),
    }

    rejected = False

    try:
        json.dumps(
            hostile,
            allow_nan=False,
        )
    except ValueError:
        rejected = True

    return check(
        "nan_json_rejected",
        rejected,
        "Non-finite JSON values must not serialize.",
    )


def run_suite() -> dict:
    tests = [
        test_r_zero(),
        test_m_two_boundary(),
        test_large_wrap(),
        test_actual_case_execution(),
        test_wrong_alpha_is_detectable(),
        test_wrong_laplacian_is_detectable(),
        test_reference_receipt_consistency(),
        test_nan_rejected_by_json_policy(),
    ]

    passed = sum(
        1
        for test in tests
        if test["passed"]
    )

    status = (
        "PASS"
        if passed == len(tests)
        else "FAIL"
    )

    return {
        "suite": SUITE,
        "status": status,
        "total_tests": len(tests),
        "passed_tests": passed,
        "failed_tests": (
            len(tests) - passed
        ),
        "tests": tests,
    }


def main() -> int:
    result = run_suite()

    print(
        json.dumps(
            result,
            indent=2,
            allow_nan=False,
        )
    )

    return (
        0
        if result["status"] == "PASS"
        else 1
    )


if __name__ == "__main__":
    sys.exit(main())
