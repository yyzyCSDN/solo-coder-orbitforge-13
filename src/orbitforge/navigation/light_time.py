from __future__ import annotations
from orbitforge.core.constants import C_KM_S


def one_way_light_time_s(range_km: float):
    if range_km < 0.0:
        raise ValueError('negative range')
    return range_km / C_KM_S


def two_way_light_time_s(uplink_range_km: float, downlink_range_km: float, transponder_delay_s: float = 0.0):
    return (uplink_range_km + downlink_range_km) / C_KM_S + transponder_delay_s


def iterate_retarded_time(position_at, receive_t: float, observer_position, tolerance_s: float = 1e-9):
    transmit_t = receive_t
    for _ in range(20):
        target = position_at(transmit_t)
        range_km = (target - observer_position).norm()
        updated = receive_t - range_km / C_KM_S
        if abs(updated - transmit_t) < tolerance_s:
            return updated, range_km
        transmit_t = updated
    return transmit_t, (position_at(transmit_t) - observer_position).norm()
