from __future__ import annotations
import math


def minimize(fn, lower, upper, tolerance=1e-8, max_iter=200):
    if upper <= lower:
        raise ValueError('invalid bounds')
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    c = upper - ratio * (upper - lower)
    d = lower + ratio * (upper - lower)
    fc = fn(c)
    fd = fn(d)
    for _ in range(max_iter):
        if upper - lower <= tolerance:
            break
        if fc < fd:
            upper, d, fd = d, c, fc
            c = upper - ratio * (upper - lower)
            fc = fn(c)
        else:
            lower, c, fc = c, d, fd
            d = lower + ratio * (upper - lower)
            fd = fn(d)
    x = 0.5 * (lower + upper)
    return x, fn(x)

def maximize(fn, lower, upper, **kwargs):
    x, negative = minimize(lambda value: -fn(value), lower, upper, **kwargs)
    return x, -negative
