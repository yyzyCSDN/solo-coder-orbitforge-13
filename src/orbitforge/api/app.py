from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Literal
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from orbitforge.core.vector import Vec3
from orbitforge.orbits.kepler import solve_kepler_elliptic
from orbitforge.maneuvers.hohmann import hohmann
from orbitforge.link.budget import free_space_loss_db
from orbitforge.environment.eclipse import eclipse_state
from orbitforge.attitude.quaternion import Quaternion
from orbitforge.storage.sqlite import Store
from orbitforge.tle import SGP4UnavailableError, TLECatalog, TLEPropagationError, load_tle_url


app = FastAPI(title='OrbitForge Mission Lab', version='1.0.0')
store = Store(':memory:')
tle_catalog = TLECatalog()


class KeplerReq(BaseModel):
    mean_anomaly: float
    eccentricity: float


class HohmannReq(BaseModel):
    r1_km: float
    r2_km: float


class LinkReq(BaseModel):
    range_km: float
    freq_hz: float


class EclipseReq(BaseModel):
    sat: list[float]
    sun: list[float]


class RotateReq(BaseModel):
    q: list[float]
    v: list[float]


class TLEIngestRequest(BaseModel):
    text: str = Field(description='Raw 2LE or 3LE catalog text. Original line pairs are retained.')


class TLEFetchRequest(BaseModel):
    url: str
    timeout_s: float = 20.0


class TLEPropagationRequest(BaseModel):
    satellite_number: int
    time_unix: float | None = None
    time_utc: datetime | None = None
    policy: Literal['as-of', 'latest_epoch'] = 'as-of'
    version_id: str | None = None


def _request_time(r: TLEPropagationRequest) -> float:
    if r.time_unix is None and r.time_utc is None:
        return datetime.now(timezone.utc).timestamp()
    if r.time_unix is not None and r.time_utc is not None:
        raise HTTPException(status_code=422, detail='provide only one of time_unix or time_utc')
    if r.time_unix is not None:
        return float(r.time_unix)
    parsed_time = r.time_utc if r.time_utc.tzinfo is not None else r.time_utc.replace(tzinfo=timezone.utc)
    return parsed_time.timestamp()


def _raw_version(version) -> dict[str, Any]:
    data = version.metadata()
    data['raw_tle'] = version.raw_tle
    data['three_line_tle'] = version.three_line_tle
    return data


def _ingest_response(result: dict[str, Any]) -> JSONResponse:
    if result['accepted'] == 0 and result['duplicate_versions'] == 0:
        status_code = 400
    elif result['accepted'] and result['rejected']:
        status_code = 207
    else:
        status_code = 200
    return JSONResponse(status_code=status_code, content=result)


@app.get('/live')
def live():
    return {'status': 'live'}


@app.get('/ready')
def ready():
    from orbitforge.tle.catalog import sgp4_available
    available = sgp4_available()
    return {
        'status': 'ready',
        'sgp4': available,
        'sgp4_fallback': 'none',
        'propagator': 'SGP4/WGS72' if available else 'unavailable; no two-body/J2 fallback is provided',
    }


@app.post('/v1/orbit/kepler')
def kepler(r: KeplerReq):
    return {'eccentric_anomaly': solve_kepler_elliptic(r.mean_anomaly, r.eccentricity)}


@app.post('/v1/maneuver/hohmann')
def h(r: HohmannReq):
    return hohmann(r.r1_km, r.r2_km)


@app.post('/v1/link/fspl')
def l(r: LinkReq):
    return {'loss_db': free_space_loss_db(r.range_km, r.freq_hz)}


@app.post('/v1/environment/eclipse')
def e(r: EclipseReq):
    return {'state': eclipse_state(Vec3(*r.sat), Vec3(*r.sun))}


@app.post('/v1/attitude/rotate')
def rotate(r: RotateReq):
    q = Quaternion(*r.q)
    v = q.rotate(Vec3(*r.v))
    return {'v': v.as_tuple()}


@app.post('/v1/tle/ingest')
def ingest_tle(r: TLEIngestRequest):
    result = tle_catalog.ingest_text(r.text)
    return _ingest_response(result)


@app.post('/v1/tle/fetch')
def fetch_tle(r: TLEFetchRequest):
    try:
        result = load_tle_url(r.url, tle_catalog, timeout=r.timeout_s)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return _ingest_response(result)


@app.get('/v1/catalog/satellites')
def list_satellites():
    return {'satellites': tle_catalog.satellites(), 'propagator': 'SGP4/WGS72'}


@app.get('/v1/catalog/satellites/{satellite_number}/versions')
def list_versions(satellite_number: int):
    try:
        versions = tle_catalog.versions(satellite_number)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        'satellite_number': satellite_number,
        'count': len(versions),
        'versions': [_raw_version(version) for version in versions],
    }


@app.get('/v1/catalog/satellites/{satellite_number}/versions/{version_id}')
def get_version(satellite_number: int, version_id: str):
    try:
        version = tle_catalog.get_version(satellite_number, version_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _raw_version(version)


@app.get('/v1/catalog/satellites/{satellite_number}/selected-version')
def selected_version(
    satellite_number: int,
    time_unix: float | None = Query(default=None),
    time_utc: datetime | None = Query(default=None),
    policy: Literal['as-of', 'latest_epoch'] = 'as-of',
    version_id: str | None = Query(default=None),
):
    if time_unix is not None and time_utc is not None:
        raise HTTPException(status_code=422, detail='provide only one of time_unix or time_utc')
    when = (
        time_unix
        if time_unix is not None
        else (
            time_utc if time_utc.tzinfo is not None else time_utc.replace(tzinfo=timezone.utc)
            if time_utc
            else datetime.now(timezone.utc)
        ).timestamp()
    )
    try:
        selection = tle_catalog.select(satellite_number, when, policy, version_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _raw_version(selection.version) | {'selection': selection.metadata()}


@app.post('/v1/tle/propagate')
def propagate_tle(r: TLEPropagationRequest):
    try:
        when = _request_time(r)
        return tle_catalog.propagate(r.satellite_number, when, r.policy, r.version_id)
    except SGP4UnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except TLEPropagationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get('/v1/system/audit')
def audit():
    return store.audit_chain()


def main():
    import uvicorn
    uvicorn.run('orbitforge.api.app:app', host='127.0.0.1', port=8080)
