from __future__ import annotations
import hashlib
import json

def create(package_version, python_version, dependencies, git_revision=None):
    payload = {
        'package_version': package_version,
        'python_version': python_version,
        'dependencies': dict(sorted(dependencies.items())),
        'git_revision': git_revision,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
    payload['digest'] = hashlib.sha256(raw).hexdigest()
    return payload

def verify(manifest):
    body = dict(manifest)
    expected = body.pop('digest')
    raw = json.dumps(body, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest() == expected

def same_environment(a, b):
    keys = ('package_version', 'python_version', 'dependencies')
    return all(a.get(key) == b.get(key) for key in keys)
