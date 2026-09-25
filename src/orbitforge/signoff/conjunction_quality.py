from __future__ import annotations

def evaluate(encounters, maximum_probability, minimum_miss_km):
    findings = []
    for encounter in encounters:
        probability = encounter.get('collision_probability', 0.0)
        miss = encounter.get('miss_distance_km', float('inf'))
        if probability > maximum_probability:
            findings.append((encounter.get('id'), 'probability', probability))
        if miss < minimum_miss_km:
            findings.append((encounter.get('id'), 'miss_distance', miss))
    return findings

def worst(encounters):
    return max(encounters, key=lambda row: row.get('collision_probability', 0.0), default=None)
