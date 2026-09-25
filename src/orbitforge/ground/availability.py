from __future__ import annotations

def combine_outages(planned, unplanned):
    intervals = sorted(planned + unplanned)
    merged = []
    for start, end in intervals:
        if end <= start:
            continue
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return [tuple(x) for x in merged]

def available_fraction(start, end, outages):
    duration = end - start
    if duration <= 0.0:
        raise ValueError('invalid interval')
    blocked = 0.0
    for a, b in combine_outages(outages, []):
        blocked += max(0.0, min(end, b) - max(start, a))
    return max(0.0, 1.0 - blocked / duration)

def is_available(epoch, outages):
    return not any(a <= epoch < b for a, b in outages)
