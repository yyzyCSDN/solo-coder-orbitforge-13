from __future__ import annotations
from collections import deque

class EWMA:

    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self.mean = None
        self.var = 0.0

    def update(self, x):
        if self.mean is None:
            self.mean = x
            return 0.0
        d = x - self.mean
        self.mean += self.alpha * d
        self.var = (1 - self.alpha) * (self.var + self.alpha * d * d)
        return d / self.var ** 0.5 if self.var > 1e-12 else 0.0

def detect_series(values, alpha=0.2, z_limit=4.0):
    m = EWMA(alpha)
    return [(i, v, z) for i, v in enumerate(values) if abs((z := m.update(v))) >= z_limit]
