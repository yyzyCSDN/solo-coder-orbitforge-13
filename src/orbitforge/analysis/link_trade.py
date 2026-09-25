from __future__ import annotations

def required_eirp_dbw(path_loss_db, gt_db_k, required_ebn0_db, bitrate_bps, implementation_loss_db=0.0):
    import math
    kb_db = -228.6
    return required_ebn0_db + 10.0 * math.log10(bitrate_bps) + path_loss_db - gt_db_k + kb_db + implementation_loss_db

def antenna_trade(options, required_eirp_dbw_value):
    feasible = []
    for option in options:
        eirp = option['tx_power_dbw'] + option['gain_dbi'] - option.get('loss_db', 0.0)
        if eirp >= required_eirp_dbw_value:
            row = dict(option)
            row['margin_db'] = eirp - required_eirp_dbw_value
            feasible.append(row)
    return sorted(feasible, key=lambda r: (r.get('mass_kg', 0.0), -r['margin_db']))
