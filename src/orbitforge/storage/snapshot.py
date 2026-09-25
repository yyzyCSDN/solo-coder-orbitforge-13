from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Snapshot:
    kind: str
    payload: dict
    digest: str

def canonical_json(payload):
    return json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False)

def make_snapshot(kind: str, payload: dict):
    raw = canonical_json(payload)
    digest = hashlib.sha256((kind + '\x00' + raw).encode()).hexdigest()
    return Snapshot(kind, json.loads(raw), digest)

def verify_snapshot(snapshot: Snapshot):
    return make_snapshot(snapshot.kind, snapshot.payload).digest == snapshot.digest

def compare_snapshots(a: Snapshot, b: Snapshot):
    keys = sorted(set(a.payload) | set(b.payload))
    return {k: (a.payload.get(k), b.payload.get(k)) for k in keys if a.payload.get(k) != b.payload.get(k)}
