from __future__ import annotations

def violations(samples, lower_k, upper_k):
    return [(t, value) for t, value in samples if value < lower_k or value > upper_k]

def excursion_durations(samples, lower_k, upper_k):
    if len(samples) < 2:
        return []
    out = []
    start = None
    state = None
    for t, value in samples:
        current = 'low' if value < lower_k else 'high' if value > upper_k else 'ok'
        if current != state:
            if state in {'low', 'high'} and start is not None:
                out.append((state, start, t, t - start))
            start = t if current in {'low', 'high'} else None
            state = current
    if state in {'low', 'high'} and start is not None:
        out.append((state, start, samples[-1][0], samples[-1][0] - start))
    return out

def max_temperature(samples):
    return max((value for _, value in samples), default=None)
