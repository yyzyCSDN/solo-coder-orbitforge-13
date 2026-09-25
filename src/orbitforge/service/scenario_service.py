from __future__ import annotations
import hashlib
import json

class ScenarioService:
    def __init__(self):
        self._records = {}

    def create(self, name, inputs, parameters):
        canonical = json.dumps({'name': name, 'inputs': inputs, 'parameters': parameters}, sort_keys=True, separators=(',', ':'))
        scenario_id = hashlib.sha256(canonical.encode()).hexdigest()[:24]
        record = {'id': scenario_id, 'name': name, 'inputs': inputs, 'parameters': parameters, 'status': 'draft'}
        self._records.setdefault(scenario_id, record)
        return dict(self._records[scenario_id])

    def freeze(self, scenario_id):
        record = self._records[scenario_id]
        if record['status'] != 'draft':
            return dict(record)
        record['status'] = 'frozen'
        return dict(record)

    def clone(self, scenario_id, new_name):
        source = self._records[scenario_id]
        return self.create(new_name, dict(source['inputs']), dict(source['parameters']))

    def list(self):
        return [dict(self._records[key]) for key in sorted(self._records)]
