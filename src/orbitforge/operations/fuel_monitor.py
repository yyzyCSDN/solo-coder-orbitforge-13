from __future__ import annotations

def estimate_remaining(initial_kg, consumed_events):
    consumed = sum(max(0.0, row['consumed_kg']) for row in consumed_events)
    return max(0.0, initial_kg - consumed)

def leak_rate_kg_day(measurements):
    if len(measurements) < 2:
        return 0.0
    ordered = sorted(measurements)
    dt_days = (ordered[-1][0] - ordered[0][0]) / 86400.0
    if dt_days <= 0.0:
        return 0.0
    return max(0.0, (ordered[0][1] - ordered[-1][1]) / dt_days)

def reserve_days(remaining_kg, daily_nominal_kg, leak_kg_day=0.0):
    rate = daily_nominal_kg + leak_kg_day
    return remaining_kg / rate if rate > 0.0 else float('inf')

def below_reserve(remaining_kg, reserve_kg):
    return remaining_kg < reserve_kg
