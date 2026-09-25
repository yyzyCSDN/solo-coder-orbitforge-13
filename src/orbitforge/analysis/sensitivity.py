from __future__ import annotations

def finite_difference(fn, params, steps):
    base = fn(**params)
    out = {}
    for k, h in steps.items():
        p = dict(params)
        p[k] += h
        q = dict(params)
        q[k] -= h
        out[k] = (fn(**p) - fn(**q)) / (2 * h)
    return (base, out)

def normalized_sensitivity(base, derivatives, params):
    return {k: derivatives[k] * params[k] / base if base else 0.0 for k in derivatives}
