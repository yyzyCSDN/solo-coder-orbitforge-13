from __future__ import annotations
import math
from orbitforge.core.constants import MU_EARTH_KM3_S2, R_EARTH_EQUATOR_KM


def circular_period_s(altitude_km):
    radius = R_EARTH_EQUATOR_KM + altitude_km
    return 2.0 * math.pi * math.sqrt(radius ** 3 / MU_EARTH_KM3_S2)

def evaluate_candidate(candidate, weights):
    altitude = candidate['altitude_km']
    period = circular_period_s(altitude)
    drag_penalty = max(0.0, (500.0 - altitude) / 500.0)
    radiation_penalty = max(0.0, (altitude - 1000.0) / 20000.0)
    coverage_reward = candidate.get('coverage_fraction', 0.0)
    revisit_penalty = candidate.get('revisit_s', period) / 86400.0
    score = (
        weights.get('coverage', 1.0) * coverage_reward
        - weights.get('revisit', 1.0) * revisit_penalty
        - weights.get('drag', 1.0) * drag_penalty
        - weights.get('radiation', 1.0) * radiation_penalty
    )
    return {
        **candidate,
        'period_s': period,
        'drag_penalty': drag_penalty,
        'radiation_penalty': radiation_penalty,
        'score': score,
    }

def rank(candidates, weights):
    evaluated = [evaluate_candidate(candidate, weights) for candidate in candidates]
    return sorted(evaluated, key=lambda row: row['score'], reverse=True)
