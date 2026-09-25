from __future__ import annotations

def health_score(metrics, limits):
    score = 100.0
    findings = []
    for name, value in metrics.items():
        rule = limits.get(name)
        if rule is None:
            continue
        low, high, weight = rule
        if value < low:
            score -= weight
            findings.append((name, 'low', value, low))
        elif value > high:
            score -= weight
            findings.append((name, 'high', value, high))
    return {'score': max(0.0, score), 'findings': findings}

def readiness(health, required_score=80.0):
    return health['score'] >= required_score and (not any((f[0] == 'battery_soc' and f[1] == 'low' for f in health['findings'])))
