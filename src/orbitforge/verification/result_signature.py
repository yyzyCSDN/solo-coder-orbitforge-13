from __future__ import annotations
import hashlib
import hmac
import json

def canonical_bytes(result):
    return json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(result):
    return hashlib.sha256(canonical_bytes(result)).hexdigest()

def sign(result, key):
    return hmac.new(key, canonical_bytes(result), hashlib.sha256).hexdigest()

def verify(result, key, signature):
    expected = sign(result, key)
    return hmac.compare_digest(expected, signature)

def envelope(result, key_id, key):
    return {
        'result': result,
        'sha256': digest(result),
        'key_id': key_id,
        'signature': sign(result, key),
    }
