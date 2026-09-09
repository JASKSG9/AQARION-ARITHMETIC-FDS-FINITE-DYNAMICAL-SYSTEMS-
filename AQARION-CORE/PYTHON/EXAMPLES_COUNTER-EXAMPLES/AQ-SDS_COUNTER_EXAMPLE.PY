def find_small_counterexample(expr, variables, bound=2):
    """
    Search integer assignments in [-bound, bound]
    that make expr nonzero.
    """
    import itertools

    for values in itertools.product(
        range(-bound, bound + 1),
        repeat=len(variables)
    ):
        assignment = dict(zip(variables, values))

        if sp.expand(expr.subs(assignment)) != 0:
            return assignment

    return None
