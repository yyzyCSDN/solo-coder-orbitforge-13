from __future__ import annotations

def evaluate(option, required_torque_nm, required_momentum_nms, pointing_error_arcsec):
    torque_margin = option['max_torque_nm'] - required_torque_nm
    momentum_margin = option['max_momentum_nms'] - required_momentum_nms
    pointing_margin = option['pointing_capability_arcsec'] - pointing_error_arcsec
    feasible = torque_margin >= 0.0 and momentum_margin >= 0.0 and pointing_margin >= 0.0
    return {
        **option,
        'torque_margin_nm': torque_margin,
        'momentum_margin_nms': momentum_margin,
        'pointing_margin_arcsec': pointing_margin,
        'feasible': feasible,
    }

def rank(options, required_torque_nm, required_momentum_nms, pointing_error_arcsec):
    rows = [evaluate(option, required_torque_nm, required_momentum_nms, pointing_error_arcsec) for option in options]
    return sorted(rows, key=lambda row: (not row['feasible'], row.get('mass_kg', 0.0), -row['pointing_margin_arcsec']))
