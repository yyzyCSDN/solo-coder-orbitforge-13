from __future__ import annotations
import hashlib
import json

def build(release_name, artifacts, scenario_snapshot, software_manifest):
    artifact_rows = []
    for name, body in sorted(artifacts.items()):
        artifact_rows.append({
            'name': name,
            'bytes': len(body),
            'sha256': hashlib.sha256(body).hexdigest(),
        })
    payload = {
        'release_name': release_name,
        'artifacts': artifact_rows,
        'scenario_snapshot': scenario_snapshot,
        'software_manifest': software_manifest,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    payload['release_sha256'] = hashlib.sha256(raw).hexdigest()
    return payload

def verify(manifest, artifacts):
    rebuilt = build(
        manifest['release_name'],
        artifacts,
        manifest['scenario_snapshot'],
        manifest['software_manifest'],
    )
    return rebuilt == manifest

def changed_artifacts(a, b):
    left = {row['name']: row['sha256'] for row in a['artifacts']}
    right = {row['name']: row['sha256'] for row in b['artifacts']}
    names = sorted(set(left) | set(right))
    return [name for name in names if left.get(name) != right.get(name)]

def summary(manifest):
    return {
        'release_name': manifest['release_name'],
        'artifact_count': len(manifest['artifacts']),
        'total_bytes': sum(row['bytes'] for row in manifest['artifacts']),
        'release_sha256': manifest['release_sha256'],
    }

def artifact_map(manifest):
    result = {}
    for row in manifest['artifacts']:
        result[row['name']] = {
            'bytes': row['bytes'],
            'sha256': row['sha256'],
        }
    return result

def has_artifact(manifest, name, digest=None):
    row = artifact_map(manifest).get(name)
    if row is None:
        return False
    if digest is None:
        return True
    return row['sha256'] == digest
