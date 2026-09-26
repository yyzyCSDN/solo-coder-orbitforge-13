from __future__ import annotations
import datetime as dt
import os
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from .model import TLEVersion
from .propagate import SGP4Propagator, SGP4_ERRORS
from .store import CatalogStore, UnknownSatelliteError

DEFAULT_STALE_AFTER_DAYS = 7.0

class TLEIn(BaseModel):
    line1: str
    line2: str
    name: str = ''

class IngestRequest(BaseModel):
    tles: list[TLEIn]
    source: str = ''

class BatchPropagateRequest(BaseModel):
    times: list[dt.datetime]
    stale_after_days: float = DEFAULT_STALE_AFTER_DAYS

def _parse_tle_text(text: str) -> list[TLEIn]:
    """Accept 2-line or 3-line (with name) TLE blocks."""
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    out, i = [], 0
    while i < len(lines):
        name = ''
        if not lines[i].startswith(('1 ', '2 ')):
            name = lines[i].strip()
            i += 1
        if i + 1 >= len(lines) or not lines[i].startswith('1 ') or not lines[i + 1].startswith('2 '):
            raise ValueError(f'malformed TLE block near line {i + 1}')
        out.append(TLEIn(name=name, line1=lines[i], line2=lines[i + 1]))
        i += 2
    return out

def _version_ref(v: TLEVersion) -> dict:
    """Identity of the exact element set used — enough to audit any result."""
    return {
        'version_id': v.version_id,
        'epoch': v.epoch.isoformat().replace('+00:00', 'Z'),
        'bstar_inv_earth_radii': v.bstar,
        'seq': v.seq,
        'ingested_at': v.ingested_at.isoformat().replace('+00:00', 'Z'),
        'source': v.source,
        'content_hash': v.content_hash,
        'line1': v.line1,
        'line2': v.line2,
    }

def build_router(store: CatalogStore, propagator: SGP4Propagator | None = None,
                 stale_after_days: float = DEFAULT_STALE_AFTER_DAYS) -> APIRouter:
    prop = propagator or SGP4Propagator()
    router = APIRouter(prefix='/v1/catalog', tags=['catalog'])

    def propagate_one(norad_id: int, when: dt.datetime, stale_days: float) -> dict:
        try:
            sel = store.select(norad_id, when)
        except UnknownSatelliteError:
            raise HTTPException(404, f'unknown satellite {norad_id}')
        result = prop.propagate(sel.version, when)
        warnings = []
        if sel.backward:
            warnings.append(
                'backward_propagation: requested time predates every catalogued '
                f'epoch; propagated backwards from epoch {sel.version.epoch.isoformat()}')
        if result.minutes_from_epoch / 1440.0 > stale_days:
            warnings.append(
                f'stale_element_set: element set is {result.minutes_from_epoch / 1440.0:.1f} days '
                f'old at requested time (threshold {stale_days} days); accuracy degrades with age')
        if result.sgp4_error and result.sgp4_error != 6:
            raise HTTPException(422, f'SGP4 failed: {SGP4_ERRORS.get(result.sgp4_error)}')
        if result.sgp4_error == 6:
            warnings.append('satellite_decayed: SGP4 reports the satellite has decayed')
        return {
            'norad_id': norad_id,
            'time': when.isoformat().replace('+00:00', 'Z'),
            'frame': result.frame,
            'position_km': list(result.position_km),
            'velocity_km_s': list(result.velocity_km_s),
            'minutes_from_epoch': result.minutes_from_epoch,
            'propagator': {**prop.info(), 'model': result.model},
            'version_used': _version_ref(sel.version),
            'warnings': warnings,
        }

    @router.post('/tles')
    async def ingest(request: Request):
        if request.headers.get('content-type', '').startswith('text/plain'):
            try:
                items = _parse_tle_text((await request.body()).decode('utf-8'))
            except ValueError as exc:
                raise HTTPException(422, str(exc))
            source = ''
        else:
            body = IngestRequest.model_validate(await request.json())
            items, source = body.tles, body.source
        results, created = [], 0
        for item in items:
            try:
                res = store.ingest(item.name, item.line1, item.line2, source=source)
            except ValueError as exc:
                results.append({'line1': item.line1, 'error': str(exc)})
                continue
            created += int(res.created)
            results.append({
                'norad_id': res.version.norad_id,
                'version_id': res.version.version_id,
                'created': res.created,
                'duplicate': not res.created,
                'epoch': res.version.epoch.isoformat().replace('+00:00', 'Z'),
                'warnings': list(res.warnings),
            })
        return {'ingested': created, 'duplicates': len(items) - created, 'results': results}

    @router.get('/satellites')
    def satellites():
        return {'satellites': store.satellites()}

    @router.get('/satellites/{norad_id}')
    def satellite(norad_id: int):
        try:
            latest = store.latest(norad_id)
        except UnknownSatelliteError:
            raise HTTPException(404, f'unknown satellite {norad_id}')
        return {'norad_id': norad_id, 'name': latest.name,
                'version_count': len(store.versions(norad_id)),
                'latest_version': latest.summary()}

    @router.get('/satellites/{norad_id}/versions')
    def versions(norad_id: int):
        try:
            vs = store.versions(norad_id)
        except UnknownSatelliteError:
            raise HTTPException(404, f'unknown satellite {norad_id}')
        latest_id = vs[-1].version_id
        return {'norad_id': norad_id,
                'versions': [{**v.summary(), 'is_latest': v.version_id == latest_id} for v in vs]}

    @router.get('/satellites/{norad_id}/propagate')
    def propagate_get(norad_id: int, time: dt.datetime,
                      stale_after_days: float = DEFAULT_STALE_AFTER_DAYS):
        return propagate_one(norad_id, time, stale_after_days)

    @router.post('/satellites/{norad_id}/propagate')
    def propagate_batch(norad_id: int, body: BatchPropagateRequest):
        return {'norad_id': norad_id,
                'states': [propagate_one(norad_id, t, body.stale_after_days) for t in body.times]}

    @router.get('/propagator')
    def propagator_info():
        return prop.info()

    return router

def default_store() -> CatalogStore:
    journal = os.environ.get('ORBITFORGE_CATALOG_JOURNAL') or None
    return CatalogStore(journal_path=journal)

router = build_router(default_store())
