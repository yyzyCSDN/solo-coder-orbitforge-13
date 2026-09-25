from __future__ import annotations

def evaluate(remaining_kg, reserve_kg, planned_burn_kg, uncertainty_fraction=0.0):
    required = reserve_kg + planned_burn_kg * (1.0 + uncertainty_fraction)
    margin = remaining_kg - required
    findings = []
    if remaining_kg < reserve_kg:
        findings.append(('below_reserve', remaining_kg, reserve_kg))
    if margin < 0.0:
        findings.append(('insufficient_for_plan', margin))
    return {'required_kg': required, 'margin_kg': margin, 'findings': findings, 'ready': not findings}

def compare(actual, previous):
    return {'margin_change_kg': actual['margin_kg'] - previous['margin_kg'], 'ready_changed': actual['ready'] != previous['ready']}
