from __future__ import annotations

def evaluate(node_temperatures, limits):
    findings = []
    for name, value in node_temperatures.items():
        if name not in limits:
            findings.append((name, 'missing_limit', value))
            continue
        low, high = limits[name]
        if value < low:
            findings.append((name, 'too_cold', value, low))
        if value > high:
            findings.append((name, 'too_hot', value, high))
    return {'findings': findings, 'ready': not findings}

def margin(node_temperatures, limits):
    out = {}
    for name, value in node_temperatures.items():
        if name in limits:
            low, high = limits[name]
            out[name] = min(value - low, high - value)
    return out
