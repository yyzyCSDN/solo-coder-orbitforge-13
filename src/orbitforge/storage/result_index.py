from __future__ import annotations

class ResultIndex:
    def __init__(self):
        self._rows = {}

    def add(self, result_id, kind, created, tags=()):
        if result_id in self._rows:
            raise ValueError('duplicate result id')
        self._rows[result_id] = {
            'id': result_id,
            'kind': kind,
            'created': created,
            'tags': frozenset(tags),
        }

    def query(self, kind=None, tag=None, created_after=None):
        rows = list(self._rows.values())
        if kind is not None:
            rows = [r for r in rows if r['kind'] == kind]
        if tag is not None:
            rows = [r for r in rows if tag in r['tags']]
        if created_after is not None:
            rows = [r for r in rows if r['created'] >= created_after]
        return sorted(rows, key=lambda r: (-r['created'], r['id']))

    def remove(self, result_id):
        return self._rows.pop(result_id, None)
