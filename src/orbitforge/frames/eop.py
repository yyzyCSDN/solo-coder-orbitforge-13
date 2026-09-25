from __future__ import annotations
from dataclasses import dataclass
from bisect import bisect_left

@dataclass(frozen=True)
class EOPSample:
    mjd: float
    xp_arcsec: float
    yp_arcsec: float
    dut1_s: float
    lod_ms: float = 0.0

class EOPSeries:

    def __init__(self, samples):
        self.samples = sorted(samples, key=lambda x: x.mjd)
        self._mjd = [s.mjd for s in self.samples]
        if len(set(self._mjd)) != len(self._mjd):
            raise ValueError('duplicate EOP date')

    def at(self, mjd: float) -> EOPSample:
        if not self.samples:
            raise ValueError('empty EOP series')
        if mjd <= self._mjd[0]:
            return self.samples[0]
        if mjd >= self._mjd[-1]:
            return self.samples[-1]
        i = bisect_left(self._mjd, mjd)
        a = self.samples[i - 1]
        b = self.samples[i]
        u = (mjd - a.mjd) / (b.mjd - a.mjd)
        return EOPSample(mjd, a.xp_arcsec + u * (b.xp_arcsec - a.xp_arcsec), a.yp_arcsec + u * (b.yp_arcsec - a.yp_arcsec), a.dut1_s + u * (b.dut1_s - a.dut1_s), a.lod_ms + u * (b.lod_ms - a.lod_ms))

    def coverage(self):
        return (self._mjd[0], self._mjd[-1])

    def gaps(self, threshold_days: float=2.0):
        return [(a, b) for a, b in zip(self._mjd, self._mjd[1:]) if b - a > threshold_days]
