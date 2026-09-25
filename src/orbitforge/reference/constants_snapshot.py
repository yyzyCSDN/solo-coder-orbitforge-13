from __future__ import annotations
from orbitforge.core import constants

def earth_constants():
    return {
        'mu_earth_km3_s2': constants.MU_EARTH_KM3_S2,
        'earth_equator_radius_km': constants.R_EARTH_EQUATOR_KM,
        'earth_polar_radius_km': constants.R_EARTH_POLAR_KM,
        'earth_j2': constants.J2_EARTH,
        'earth_rotation_rad_s': constants.OMEGA_EARTH_RAD_S,
        'speed_of_light_km_s': constants.C_KM_S,
        'astronomical_unit_km': constants.AU_KM,
    }

def fingerprint():
    import hashlib
    import json
    raw = json.dumps(earth_constants(), sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()
