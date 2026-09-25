from __future__ import annotations
import hashlib
import io
import json
import zipfile

def build_bundle(files, metadata):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        manifest = []
        for name, data in sorted(files.items()):
            digest = hashlib.sha256(data).hexdigest()
            manifest.append({'name': name, 'size': len(data), 'sha256': digest})
            archive.writestr(name, data)
        archive.writestr('metadata.json', json.dumps(metadata, sort_keys=True, indent=2))
        archive.writestr('manifest.json', json.dumps(manifest, sort_keys=True, indent=2))
    return buffer.getvalue()

def inspect_bundle(data):
    with zipfile.ZipFile(io.BytesIO(data), 'r') as archive:
        manifest = json.loads(archive.read('manifest.json'))
        mismatches = []
        for row in manifest:
            body = archive.read(row['name'])
            if len(body) != row['size'] or hashlib.sha256(body).hexdigest() != row['sha256']:
                mismatches.append(row['name'])
        metadata = json.loads(archive.read('metadata.json'))
    return {'metadata': metadata, 'manifest': manifest, 'mismatches': mismatches}
