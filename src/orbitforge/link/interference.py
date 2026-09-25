from __future__ import annotations
import math


def db_to_linear(db):
    return 10.0 ** (db / 10.0)

def linear_to_db(value):
    if value <= 0.0:
        return float('-inf')
    return 10.0 * math.log10(value)

def combine_interference_dbw(levels_dbw):
    return linear_to_db(sum(db_to_linear(level) for level in levels_dbw))

def carrier_to_interference_db(carrier_dbw, interference_levels_dbw):
    if not interference_levels_dbw:
        return float('inf')
    return carrier_dbw - combine_interference_dbw(interference_levels_dbw)

def effective_cn0_dbhz(carrier_dbw, noise_dbw_hz, interference_dbw_hz):
    combined = linear_to_db(db_to_linear(noise_dbw_hz) + db_to_linear(interference_dbw_hz))
    return carrier_dbw - combined
