from __future__ import annotations
import hashlib
import json
import time

class AuditLog:
    def __init__(self):
        self.entries = []
        self.head = '0' * 64

    def append(self, actor, action, subject, details):
        body = {
            'actor': actor,
            'action': action,
            'subject': subject,
            'details': details,
            'created': time.time(),
            'previous': self.head,
        }
        raw = json.dumps(body, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
        body['digest'] = hashlib.sha256(raw).hexdigest()
        self.entries.append(body)
        self.head = body['digest']
        return dict(body)

    def verify(self):
        previous = '0' * 64
        for entry in self.entries:
            body = dict(entry)
            digest = body.pop('digest')
            if body['previous'] != previous:
                return False
            raw = json.dumps(body, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
            if hashlib.sha256(raw).hexdigest() != digest:
                return False
            previous = digest
        return True
