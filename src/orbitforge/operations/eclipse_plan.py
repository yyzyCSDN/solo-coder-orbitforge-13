from __future__ import annotations


def eclipse_segments(samples):
    segments = []
    start = None
    previous_t = None
    previous_state = None
    for t, state in samples:
        dark = state != 'sunlit'
        if dark and start is None:
            start = t
        if not dark and start is not None:
            segments.append((start, t, previous_state))
            start = None
        previous_t = t
        previous_state = state
    if start is not None and previous_t is not None:
        segments.append((start, previous_t, previous_state))
    return segments

def longest_eclipse_s(samples):
    return max((end - start for start, end, _ in eclipse_segments(samples)), default=0.0)

def dark_fraction(samples):
    if not samples:
        return 0.0
    return sum(1 for _, state in samples if state != 'sunlit') / len(samples)
