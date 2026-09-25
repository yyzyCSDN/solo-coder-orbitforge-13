from __future__ import annotations
import hashlib
import json


def create(project_name, configuration, inputs, software_version):
    payload = {
        'project_name': project_name,
        'configuration': configuration,
        'inputs': inputs,
        'software_version': software_version,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    payload['snapshot_id'] = hashlib.sha256(raw).hexdigest()
    return payload

def verify(snapshot):
    body = dict(snapshot)
    expected = body.pop('snapshot_id')
    raw = json.dumps(body, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest() == expected

def diff(a, b):
    keys = sorted(set(a) | set(b))
    return {key: (a.get(key), b.get(key)) for key in keys if a.get(key) != b.get(key)}
