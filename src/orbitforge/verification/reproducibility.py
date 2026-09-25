from __future__ import annotations
import hashlib
import json


def analysis_identity(kind, inputs, parameters, software_version):
    payload = {
        'kind': kind,
        'inputs': inputs,
        'parameters': parameters,
        'software_version': software_version,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def compare_manifests(a, b):
    keys = sorted(set(a) | set(b))
    return {key: (a.get(key), b.get(key)) for key in keys if a.get(key) != b.get(key)}


def deterministic_seed(identity):
    return int(identity[:16], 16)
