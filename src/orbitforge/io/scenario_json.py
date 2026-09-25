from __future__ import annotations
import json
import hashlib

REQUIRED_TOP_LEVEL = {'spacecraft','epoch','analysis'}

def loads(text):
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError('scenario must be an object')
    missing = REQUIRED_TOP_LEVEL - set(payload)
    if missing:
        raise ValueError('missing scenario keys: ' + ','.join(sorted(missing)))
    return payload

def dumps(payload):
    return json.dumps(payload, sort_keys=True, indent=2, allow_nan=False) + '\\n'
def canonical_bytes(payload):
    return json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def fingerprint(payload):
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()

def merge(base, override):
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = value
    return result
