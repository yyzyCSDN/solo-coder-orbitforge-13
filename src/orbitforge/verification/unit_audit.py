from __future__ import annotations

UNITS = {
    'distance': {'km': 1.0, 'm': 0.001},
    'speed': {'km/s': 1.0, 'm/s': 0.001},
    'angle': {'rad': 1.0, 'deg': 0.017453292519943295},
    'time': {'s': 1.0, 'ms': 0.001, 'day': 86400.0},
}

def convert(value, category, source, target):
    table = UNITS[category]
    return value * table[source] / table[target]

def audit_fields(record, schema):
    findings = []
    for field, specification in schema.items():
        if field not in record:
            findings.append((field, 'missing'))
            continue
        category, unit = specification
        if unit not in UNITS.get(category, {}):
            findings.append((field, 'unknown_unit'))
    return findings

def compatible(category, unit_a, unit_b):
    table = UNITS.get(category, {})
    return unit_a in table and unit_b in table
