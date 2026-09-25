from __future__ import annotations

def numeric_diff(reference, candidate, tolerances):
    findings = []
    for key, ref in reference.items():
        if key not in candidate:
            findings.append((key, 'missing', ref, None))
            continue
        value = candidate[key]
        tolerance = tolerances.get(key, 0.0)
        if isinstance(ref, (int, float)) and isinstance(value, (int, float)):
            if abs(value - ref) > tolerance:
                findings.append((key, 'numeric', ref, value))
        elif value != ref:
            findings.append((key, 'changed', ref, value))
    for key, value in candidate.items():
        if key not in reference:
            findings.append((key, 'added', None, value))
    return findings

def pass_regression(reference, candidate, tolerances):
    return not numeric_diff(reference, candidate, tolerances)
