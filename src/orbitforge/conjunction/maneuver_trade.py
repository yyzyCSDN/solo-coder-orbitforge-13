from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AvoidanceCandidate:
    name: str
    delta_v_m_s: float
    miss_distance_km: float
    collision_probability: float
    mission_cost: float

def feasible(candidates, max_delta_v_m_s, max_probability, min_miss_km):
    return [c for c in candidates if c.delta_v_m_s <= max_delta_v_m_s and c.collision_probability <= max_probability and c.miss_distance_km >= min_miss_km]

def rank(candidates, probability_weight=1.0, fuel_weight=0.1, mission_weight=0.5):
    return sorted(candidates, key=lambda c: (probability_weight * c.collision_probability * 1e6 + fuel_weight * c.delta_v_m_s + mission_weight * c.mission_cost, -c.miss_distance_km))

def best_candidate(candidates, **kwargs):
    ranked = rank(feasible(candidates, kwargs.pop('max_delta_v_m_s'), kwargs.pop('max_probability'), kwargs.pop('min_miss_km')), **kwargs)
    return ranked[0] if ranked else None
