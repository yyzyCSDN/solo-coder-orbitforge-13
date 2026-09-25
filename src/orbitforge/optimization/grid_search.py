from __future__ import annotations
import itertools


def parameter_grid(space):
    keys = list(space)
    for values in itertools.product(*(space[key] for key in keys)):
        yield dict(zip(keys, values))

def search(space, objective, constraints=()):
    feasible = []
    rejected = []
    for parameters in parameter_grid(space):
        failures = [name for name, predicate in constraints if not predicate(parameters)]
        if failures:
            rejected.append((parameters, failures))
            continue
        score = objective(parameters)
        feasible.append((score, parameters))
    feasible.sort(key=lambda row: row[0])
    return feasible, rejected

def best(space, objective, constraints=()):
    feasible, rejected = search(space, objective, constraints)
    return (feasible[0] if feasible else None), rejected
