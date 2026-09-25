from __future__ import annotations

def replay(initial_state, epochs, propagator):
    states = [initial_state]
    current = initial_state
    for epoch in epochs:
        dt = epoch - current.epoch_tai_s
        current = propagator(current, dt)
        states.append(current)
    return states

def compare(reference, candidate, position_tolerance_km, velocity_tolerance_km_s):
    if len(reference) != len(candidate):
        return {'equal': False, 'reason': 'length'}
    worst_position = 0.0
    worst_velocity = 0.0
    for a, b in zip(reference, candidate):
        worst_position = max(worst_position, (a.position_km - b.position_km).norm())
        worst_velocity = max(worst_velocity, (a.velocity_km_s - b.velocity_km_s).norm())
    return {
        'equal': worst_position <= position_tolerance_km and worst_velocity <= velocity_tolerance_km_s,
        'worst_position_km': worst_position,
        'worst_velocity_km_s': worst_velocity,
    }
