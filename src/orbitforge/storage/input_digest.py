from __future__ import annotations
import hashlib
import json

def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()

def digest_json(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return digest_bytes(raw)

def digest_inputs(files, metadata):
    return {
        'files': {name: digest_bytes(body) for name, body in sorted(files.items())},
        'metadata': digest_json(metadata),
    }

def equal(a, b):
    return a == b
