from __future__ import annotations

def require_fields(payload, fields):
    missing = [field for field in fields if field not in payload]
    if missing:
        raise ValueError('missing fields: ' + ','.join(missing))
    return payload

def finite_numbers(payload, fields):
    import math
    bad = []
    for field in fields:
        value = payload.get(field)
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            bad.append(field)
    if bad:
        raise ValueError('non-finite numeric fields: ' + ','.join(bad))
    return payload

def bounded(payload, rules):
    violations = []
    for field, (low, high) in rules.items():
        value = payload[field]
        if not low <= value <= high:
            violations.append((field, value, low, high))
    if violations:
        raise ValueError(f'out of bounds: {violations}')
    return payload
