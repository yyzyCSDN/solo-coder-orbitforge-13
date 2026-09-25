from __future__ import annotations

def compare(reference, candidate, absolute_tolerances=None, relative_tolerances=None):
    absolute_tolerances = absolute_tolerances or {}
    relative_tolerances = relative_tolerances or {}
    findings = []
    keys = sorted(set(reference) | set(candidate))
    for key in keys:
        if key not in reference:
            findings.append((key, 'added', None, candidate[key]))
            continue
        if key not in candidate:
            findings.append((key, 'missing', reference[key], None))
            continue
        a = reference[key]
        b = candidate[key]
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            atol = absolute_tolerances.get(key, 0.0)
            rtol = relative_tolerances.get(key, 0.0)
            limit = atol + rtol * abs(a)
            if abs(b - a) > limit:
                findings.append((key, 'numeric', a, b))
        elif a != b:
            findings.append((key, 'changed', a, b))
    return findings
