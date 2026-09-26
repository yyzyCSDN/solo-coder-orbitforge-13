from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
import hashlib
from orbitforge.io.tle import TLERecord

def tle_content_hash(line1: str, line2: str) -> str:
    """Stable content address for one TLE set (the two 69-char lines)."""
    return hashlib.sha1(f'{line1}\n{line2}'.encode('utf-8')).hexdigest()

@dataclass(frozen=True)
class TLEVersion:
    """One immutable, originally-ingested TLE element set for a satellite.

    Versions are never mutated or dropped: stale and superseded element sets
    stay in the catalog so every propagation can name the exact data it used.
    """
    version_id: str          # '{norad_id}:{content_hash[:12]}'
    norad_id: int
    name: str
    line1: str
    line2: str
    record: TLERecord        # parsed elements, incl. BSTAR
    epoch: dt.datetime       # UTC, from the TLE epoch field
    seq: int                 # global ingestion sequence (arrival order)
    ingested_at: dt.datetime
    source: str = ''

    @property
    def bstar(self) -> float:
        return self.record.bstar_inv_earth_radii

    @property
    def content_hash(self) -> str:
        return tle_content_hash(self.line1, self.line2)

    def summary(self) -> dict:
        return {
            'version_id': self.version_id,
            'norad_id': self.norad_id,
            'name': self.name,
            'epoch': self.epoch.isoformat().replace('+00:00', 'Z'),
            'bstar_inv_earth_radii': self.bstar,
            'mean_motion_rev_day': self.record.mean_motion_rev_day,
            'element_set_number': self.record.element_set_number,
            'seq': self.seq,
            'ingested_at': self.ingested_at.isoformat().replace('+00:00', 'Z'),
            'source': self.source,
            'content_hash': self.content_hash,
            'line1': self.line1,
            'line2': self.line2,
        }

@dataclass(frozen=True)
class IngestResult:
    version: TLEVersion
    created: bool            # False when the exact TLE was already catalogued
    warnings: tuple[str, ...] = ()

@dataclass(frozen=True)
class Selection:
    """The version chosen to serve a propagation request at `when`."""
    version: TLEVersion
    backward: bool           # True when `when` predates every catalogued epoch
    age_days: float          # (when - epoch) in days; negative if backward
