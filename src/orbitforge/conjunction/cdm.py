from __future__ import annotations
import json

def normalize_cdm(payload):
    required = ['tca', 'miss_distance_km', 'relative_speed_km_s']
    missing = [k for k in required if k not in payload]
    if missing:
        raise ValueError('missing CDM fields: ' + ','.join(missing))
    result = dict(payload)
    result['tca'] = float(result['tca'])
    result['miss_distance_km'] = float(result['miss_distance_km'])
    result['relative_speed_km_s'] = float(result['relative_speed_km_s'])
    return result

def cdm_fingerprint(payload):
    import hashlib
    norm = normalize_cdm(payload)
    raw = json.dumps(norm, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()

def rank_cdm(payload):
    p = normalize_cdm(payload)
    score = max(0.0, 10.0 - p['miss_distance_km']) + min(10.0, p.get('collision_probability', 0.0) * 100000.0)
    return score
