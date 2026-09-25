from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class VersionedValue:
    key: str
    revision: int
    value: object

class VersionedStore:
    def __init__(self):
        self._latest = {}
        self._history = {}

    def put(self, key, value, expected_revision=None):
        current = self._latest.get(key)
        current_revision = current.revision if current else 0
        if expected_revision is not None and expected_revision != current_revision:
            raise ValueError('revision conflict')
        item = VersionedValue(key, current_revision + 1, value)
        self._latest[key] = item
        self._history.setdefault(key, []).append(item)
        return item

    def get(self, key, revision=None):
        if revision is None:
            return self._latest.get(key)
        return next((x for x in self._history.get(key, []) if x.revision == revision), None)

    def history(self, key):
        return list(self._history.get(key, []))
