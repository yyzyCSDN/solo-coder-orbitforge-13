from __future__ import annotations
import hashlib
import json

class SignoffService:
    def __init__(self):
        self._reviews = {}

    def create_review(self, scenario_id, findings):
        payload = {'scenario_id': scenario_id, 'findings': findings}
        raw = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
        review_id = hashlib.sha256(raw).hexdigest()[:24]
        blocking = [f for f in findings if f.get('severity', 'error') == 'error']
        record = {'id': review_id, 'scenario_id': scenario_id, 'findings': findings, 'status': 'blocked' if blocking else 'ready'}
        self._reviews[review_id] = record
        return dict(record)

    def approve(self, review_id, approver):
        record = self._reviews[review_id]
        if record['status'] != 'ready':
            raise ValueError('review is not ready')
        record['status'] = 'approved'
        record['approver'] = approver
        return dict(record)

    def get(self, review_id):
        return dict(self._reviews[review_id])
