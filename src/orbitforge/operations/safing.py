from __future__ import annotations

def safing_decision(battery_soc, thermal_c, attitude_error_deg, comm_age_s):
    reasons = []
    if battery_soc < 0.15:
        reasons.append('low_battery')
    if thermal_c > 75:
        reasons.append('overtemperature')
    if attitude_error_deg > 25:
        reasons.append('lost_pointing')
    if comm_age_s > 86400:
        reasons.append('comm_timeout')
    return {'safe_mode': bool(reasons), 'reasons': reasons}

def recovery_ready(battery_soc, thermal_c, attitude_error_deg):
    return battery_soc > 0.35 and thermal_c < 60 and (attitude_error_deg < 5)
