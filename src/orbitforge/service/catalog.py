from __future__ import annotations

class ObjectCatalog:
    def __init__(self):
        self._objects = {}

    def put(self, object_id, metadata):
        if not object_id:
            raise ValueError('object id required')
        record = dict(metadata)
        record['object_id'] = object_id
        self._objects[object_id] = record
        return dict(record)

    def get(self, object_id):
        record = self._objects.get(object_id)
        return None if record is None else dict(record)

    def search(self, predicate):
        return [dict(record) for record in self._objects.values() if predicate(record)]

    def remove(self, object_id):
        return self._objects.pop(object_id, None)

    def ids(self):
        return sorted(self._objects)
