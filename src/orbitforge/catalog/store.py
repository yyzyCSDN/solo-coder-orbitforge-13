from __future__ import annotations
import datetime as dt
import json
import os
from bisect import insort
from orbitforge.io.tle import parse, epoch_datetime
from .model import TLEVersion, IngestResult, Selection, tle_content_hash

class UnknownSatelliteError(KeyError):
    pass

def _utc(value: dt.datetime) -> dt.datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=dt.timezone.utc)
    return value.astimezone(dt.timezone.utc)

class CatalogStore:
    """Versioned TLE catalog.

    - Every distinct element set is kept forever as an immutable TLEVersion.
    - Re-ingesting identical lines is a no-op that returns the existing version
      (duplicate suppression).
    - Versions are ordered by TLE *epoch*, never by arrival time, so daily
      drops that straddle midnight or arrive out of order still sort correctly.
    - An optional JSONL journal makes the catalog durable across restarts.
    """

    def __init__(self, journal_path: str | None = None):
        self._by_norad: dict[int, list[TLEVersion]] = {}
        self._by_hash: dict[str, TLEVersion] = {}
        self._seq = 0
        self._journal_path = journal_path
        self._journal = None
        if journal_path:
            if os.path.exists(journal_path):
                with open(journal_path, 'r', encoding='utf-8') as fh:
                    for line in fh:
                        line = line.strip()
                        if line:
                            self._ingest_record(json.loads(line), journal=False)
            self._journal = open(journal_path, 'a', encoding='utf-8')

    def close(self):
        if self._journal:
            self._journal.close()
            self._journal = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # -- ingestion ------------------------------------------------------

    def ingest(self, name: str, line1: str, line2: str, source: str = '',
               ingested_at: dt.datetime | None = None) -> IngestResult:
        # Raises ValueError on malformed lines / checksum mismatch before
        # anything is stored or journaled.
        return self._ingest_record({
            'name': name,
            'line1': line1.rstrip('\r\n'),
            'line2': line2.rstrip('\r\n'),
            'source': source,
            'ingested_at': _utc(ingested_at or dt.datetime.now(dt.timezone.utc)).isoformat(),
        }, journal=True)

    def _ingest_record(self, item: dict, journal: bool) -> IngestResult:
        line1, line2 = item['line1'], item['line2']
        digest = tle_content_hash(line1, line2)
        existing = self._by_hash.get(digest)
        if existing is not None:
            return IngestResult(existing, created=False)
        record = parse(item['name'], line1, line2)
        epoch = epoch_datetime(record)
        self._seq += 1
        version = TLEVersion(
            version_id=f'{record.satellite_number}:{digest[:12]}',
            norad_id=record.satellite_number,
            name=record.name,
            line1=line1,
            line2=line2,
            record=record,
            epoch=epoch,
            seq=self._seq,
            ingested_at=_utc(dt.datetime.fromisoformat(item['ingested_at'])),
            source=item.get('source', ''),
        )
        versions = self._by_norad.setdefault(version.norad_id, [])
        insort(versions, version, key=lambda v: (v.epoch, v.seq))
        self._by_hash[digest] = version
        warnings = []
        for other in versions:
            if other is not version and other.epoch == epoch:
                warnings.append(
                    'epoch_conflict: another element set with the same epoch '
                    f'({epoch.isoformat()}) but different content exists; '
                    'the later-ingested set wins selection')
                break
        if versions[-1] is not version:
            warnings.append(
                'stale_on_arrival: epoch is older than the catalogued latest; '
                'kept as history, not used for future queries')
        if journal and self._journal:
            self._journal.write(json.dumps(item) + '\n')
            self._journal.flush()
        return IngestResult(version, created=True, warnings=tuple(warnings))

    # -- queries --------------------------------------------------------

    def _versions_or_raise(self, norad_id: int) -> list[TLEVersion]:
        versions = self._by_norad.get(norad_id)
        if not versions:
            raise UnknownSatelliteError(norad_id)
        return versions

    def versions(self, norad_id: int) -> list[TLEVersion]:
        """All catalogued versions, oldest epoch first."""
        return list(self._versions_or_raise(norad_id))

    def latest(self, norad_id: int) -> TLEVersion:
        return self._versions_or_raise(norad_id)[-1]

    def get_version(self, version_id: str) -> TLEVersion | None:
        for versions in self._by_norad.values():
            for v in versions:
                if v.version_id == version_id:
                    return v
        return None

    def select(self, norad_id: int, when: dt.datetime) -> Selection:
        """Pick the version to propagate for time `when`.

        As-of rule: the newest element set whose epoch is <= `when` (ties go
        to the later-ingested set). If `when` predates every epoch, fall back
        to the oldest set and flag the selection as backward propagation.
        """
        when = _utc(when)
        versions = self._versions_or_raise(norad_id)
        chosen = versions[0]
        backward = True
        for v in versions:
            if v.epoch <= when:
                chosen, backward = v, False
            else:
                break
        age = (when - chosen.epoch).total_seconds() / 86400.0
        return Selection(chosen, backward, age)

    def satellites(self) -> list[dict]:
        out = []
        for norad_id, versions in sorted(self._by_norad.items()):
            out.append({
                'norad_id': norad_id,
                'name': versions[-1].name,
                'version_count': len(versions),
                'oldest_epoch': versions[0].epoch.isoformat().replace('+00:00', 'Z'),
                'latest_epoch': versions[-1].epoch.isoformat().replace('+00:00', 'Z'),
                'latest_version_id': versions[-1].version_id,
            })
        return out
