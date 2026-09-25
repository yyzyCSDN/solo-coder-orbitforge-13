from __future__ import annotations
import hashlib
import json

def file_digest(data: bytes):
    return hashlib.sha256(data).hexdigest()

def build_manifest(files):
    entries = []
    for name, data in sorted(files.items()):
        entries.append({'name': name, 'bytes': len(data), 'sha256': file_digest(data)})
    raw = json.dumps(entries, sort_keys=True, separators=(',', ':')).encode()
    return {'entries': entries, 'manifest_sha256': hashlib.sha256(raw).hexdigest()}

def verify_manifest(files, manifest):
    expected = build_manifest(files)
    return expected == manifest
