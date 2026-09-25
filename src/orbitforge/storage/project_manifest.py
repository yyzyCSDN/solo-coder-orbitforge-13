from __future__ import annotations
import hashlib
import json

def build(project_name, files, dependencies, configuration_digest):
    entries = []
    for name, body in sorted(files.items()):
        entries.append({'name': name, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()})
    manifest = {
        'project': project_name,
        'files': entries,
        'dependencies': dict(sorted(dependencies.items())),
        'configuration_digest': configuration_digest,
    }
    raw = json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()
    manifest['manifest_sha256'] = hashlib.sha256(raw).hexdigest()
    return manifest

def verify(manifest, files):
    rebuilt = build(manifest['project'], files, manifest['dependencies'], manifest['configuration_digest'])
    return rebuilt == manifest
