from __future__ import annotations
import hashlib
import json

def evidence_record(kind, inputs, outputs, configuration):
    body = {
        'kind': kind,
        'inputs': inputs,
        'outputs': outputs,
        'configuration': configuration,
    }
    raw = json.dumps(body, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    body['digest'] = hashlib.sha256(raw).hexdigest()
    return body

def chain(records):
    previous = '0' * 64
    out = []
    for record in records:
        raw = json.dumps(record, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        digest = hashlib.sha256(previous.encode() + raw).hexdigest()
        out.append({'previous': previous, 'digest': digest, 'record': record})
        previous = digest
    return out

def verify_chain(entries):
    previous = '0' * 64
    for entry in entries:
        raw = json.dumps(entry['record'], sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        digest = hashlib.sha256(previous.encode() + raw).hexdigest()
        if entry['previous'] != previous or entry['digest'] != digest:
            return False
        previous = digest
    return True
