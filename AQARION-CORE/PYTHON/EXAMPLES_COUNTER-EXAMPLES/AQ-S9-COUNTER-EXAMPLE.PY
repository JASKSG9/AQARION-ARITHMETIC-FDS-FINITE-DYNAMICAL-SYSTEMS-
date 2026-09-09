vars_s9 = [
    rP, rQ, rM, rU,
    rJP, rJQ,
    rJM, rJU,
    rMeet, rJT,
]

bad = residual(
    sT,
    s0 + delta - mT
)

print(
    find_small_counterexample(
        bad,
        vars_s9,
        bound=1
    )
)
