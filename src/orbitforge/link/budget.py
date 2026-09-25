from __future__ import annotations
import math
KB_DBW_HZ_K = -228.6

def free_space_loss_db(range_km: float, freq_hz: float) -> float:
    if range_km <= 0 or freq_hz <= 0:
        raise ValueError('positive range/frequency')
    return 20 * math.log10(range_km * 1000) + 20 * math.log10(freq_hz) - 147.55221677811662

def received_power_dbw(tx_power_dbw: float, tx_gain_dbi: float, rx_gain_dbi: float, range_km: float, freq_hz: float, losses_db: float=0.0):
    return tx_power_dbw + tx_gain_dbi + rx_gain_dbi - free_space_loss_db(range_km, freq_hz) - losses_db

def cn0_dbhz(pr_dbw: float, system_temp_k: float):
    return pr_dbw - KB_DBW_HZ_K - 10 * math.log10(system_temp_k)

def ebn0_db(cn0: float, bitrate_bps: float):
    return cn0 - 10 * math.log10(bitrate_bps)

def margin_db(ebn0: float, required: float):
    return ebn0 - required
