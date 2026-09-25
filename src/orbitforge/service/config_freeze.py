from __future__ import annotations
import hashlib
import json

def freeze(configuration):
    raw = json.dumps(configuration, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return {
        'configuration': json.loads(raw),
        'digest': hashlib.sha256(raw.encode()).hexdigest(),
    }

def verify(snapshot):
    raw = json.dumps(snapshot['configuration'], sort_keys=True, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest() == snapshot['digest']

def changed(a, b):
    return a['digest'] != b['digest']
