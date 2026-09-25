from __future__ import annotations
import hashlib
import json

def snapshot(dependencies, python_version, platform_name):
    payload = {
        'dependencies': dict(sorted(dependencies.items())),
        'python_version': python_version,
        'platform': platform_name,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
    payload['digest'] = hashlib.sha256(raw).hexdigest()
    return payload

def compatible(a, b, allow_patch_drift=True):
    if a['python_version'] != b['python_version'] or a['platform'] != b['platform']:
        return False
    if not allow_patch_drift:
        return a['dependencies'] == b['dependencies']
    def major_minor(version):
        parts = str(version).split('.')
        return tuple(parts[:2])
    keys = set(a['dependencies']) | set(b['dependencies'])
    return all(key in a['dependencies'] and key in b['dependencies'] and major_minor(a['dependencies'][key]) == major_minor(b['dependencies'][key]) for key in keys)
