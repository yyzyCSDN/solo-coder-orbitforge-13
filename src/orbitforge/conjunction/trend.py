from __future__ import annotations

def miss_distance_trend(cdm_history):
    ordered = sorted(cdm_history, key=lambda x: x['created'])
    return [(row['created'], row['miss_distance_km']) for row in ordered]

def probability_trend(cdm_history):
    ordered = sorted(cdm_history, key=lambda x: x['created'])
    return [(row['created'], row.get('collision_probability', 0.0)) for row in ordered]

def worsening(cdm_history):
    if len(cdm_history) < 2:
        return False
    miss = miss_distance_trend(cdm_history)
    probability = probability_trend(cdm_history)
    return miss[-1][1] < miss[0][1] and probability[-1][1] > probability[0][1]

def latest(cdm_history):
    return max(cdm_history, key=lambda x: x['created']) if cdm_history else None
