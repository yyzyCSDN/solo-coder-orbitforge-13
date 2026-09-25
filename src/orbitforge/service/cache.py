from __future__ import annotations
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity=128):
        if capacity <= 0:
            raise ValueError('positive capacity')
        self.capacity = capacity
        self._data = OrderedDict()

    def get(self, key, default=None):
        if key not in self._data:
            return default
        value = self._data.pop(key)
        self._data[key] = value
        return value

    def put(self, key, value):
        if key in self._data:
            self._data.pop(key)
        self._data[key] = value
        evicted = None
        if len(self._data) > self.capacity:
            evicted = self._data.popitem(last=False)
        return evicted

    def invalidate(self, predicate):
        keys = [key for key, value in self._data.items() if predicate(key, value)]
        for key in keys:
            del self._data[key]
        return keys
