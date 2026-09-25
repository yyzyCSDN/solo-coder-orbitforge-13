from __future__ import annotations

def evaluate(plan):
    contacts = plan.get('contacts', 0)
    command_load = plan.get('commands', 0)
    staffing_hours = plan.get('staffing_hours', 0.0)
    autonomy_fraction = plan.get('autonomy_fraction', 0.0)
    unresolved_risks = plan.get('unresolved_risks', 0)
    score = (
        2.0 * contacts
        - 0.02 * command_load
        - 0.5 * staffing_hours
        + 20.0 * autonomy_fraction
        - 10.0 * unresolved_risks
    )
    return {**plan, 'score': score}

def rank(plans):
    return sorted((evaluate(plan) for plan in plans), key=lambda row: row['score'], reverse=True)
