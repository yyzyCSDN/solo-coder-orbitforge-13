from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    t: float
    value: float
    direction: int

def find_zero_crossings(fn, start: float, end: float, step: float, tolerance: float=1e-06):
    events = []
    ta = start
    fa = fn(ta)
    tb = ta + step
    while tb <= end + 1e-12:
        fb = fn(min(tb, end))
        if fa == 0.0:
            events.append(Event(ta, 0.0, 0))
        elif fa * fb < 0.0:
            lo, hi = (ta, min(tb, end))
            flo, fhi = (fa, fb)
            for _ in range(80):
                mid = (lo + hi) / 2.0
                fm = fn(mid)
                if abs(fm) < tolerance or hi - lo < tolerance:
                    lo = hi = mid
                    break
                if flo * fm <= 0.0:
                    hi, fhi = (mid, fm)
                else:
                    lo, flo = (mid, fm)
            t = (lo + hi) / 2.0
            direction = 1 if fb > fa else -1
            events.append(Event(t, fn(t), direction))
        ta, fa = (min(tb, end), fb)
        tb += step
    return events

def extrema_by_sampling(fn, start: float, end: float, step: float):
    samples = []
    t = start
    while t <= end + 1e-12:
        samples.append((t, fn(t)))
        t += step
    peaks = []
    for a, b, c in zip(samples, samples[1:], samples[2:]):
        if b[1] >= a[1] and b[1] >= c[1]:
            peaks.append(('max', b[0], b[1]))
        if b[1] <= a[1] and b[1] <= c[1]:
            peaks.append(('min', b[0], b[1]))
    return peaks
