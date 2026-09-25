from __future__ import annotations

class AnalysisRegistry:
    def __init__(self):
        self._handlers = {}

    def register(self, name, handler):
        if not name:
            raise ValueError('analysis name required')
        if name in self._handlers:
            raise ValueError('duplicate analysis')
        self._handlers[name] = handler

    def names(self):
        return sorted(self._handlers)

    def execute(self, name, payload):
        if name not in self._handlers:
            raise KeyError(name)
        return self._handlers[name](payload)

    def describe(self):
        return [{'name': name, 'module': handler.__module__, 'callable': handler.__name__} for name, handler in sorted(self._handlers.items())]
