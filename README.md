# OrbitForge Mission Lab

OrbitForge is a Python library and small HTTP service for spacecraft mission
analysis: orbital mechanics, mission geometry and resource products.

## Quick start

```bash
python -m pip install -e '.[test]'
PYTHONPATH=src python -m pytest -q
orbitforge
```

## Satellite TLE catalog

The TLE service uses the official [`sgp4`](https://pypi.org/project/sgp4/)
implementation with WGS72 constants. It does not substitute the existing
two-body or J2 code for SGP4 propagation. Results are returned in the SGP4
native TEME frame in kilometres and kilometres/second.

Catalog rules:

- Every distinct raw TLE line pair is retained as an immutable version. The
  version id is a deterministic SHA-256 prefix of the exact line pair.
- Versions are ordered by the epoch parsed from line 1, not ingestion order,
  so day/year rollovers and out-of-order updates work correctly.
- Exact duplicate line pairs are ignored; separate element versions for the
  same NORAD number remain available.
- A version older than 14 days at query time is retained but marked stale.
  The stale threshold is configurable on `TLECatalog`.

Ingest a real 2LE/3LE source by pasting its contents or fetching it over
HTTP(S), then query or propagate it:

```bash
curl -X POST http://127.0.0.1:8080/v1/tle/ingest \
  -H 'content-type: application/json' \
  -d '{"text":"ISS (ZARYA)\n1 ...\n2 ...\n"}'

curl -X POST http://127.0.0.1:8080/v1/tle/fetch \
  -H 'content-type: application/json' \
  -d '{"url":"https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"}'

curl 'http://127.0.0.1:8080/v1/catalog/satellites/25544/versions'
curl 'http://127.0.0.1:8080/v1/catalog/satellites/25544/selected-version?time_utc=2026-09-26T12:00:00Z'
curl -X POST http://127.0.0.1:8080/v1/tle/propagate \
  -H 'content-type: application/json' \
  -d '{"satellite_number":25544,"time_unix":1790462400,"policy":"as-of"}'
```

The default `as-of` policy uses the newest version whose TLE epoch is not later
than the requested time. If no such epoch exists, it uses the earliest version
and emits a forward-propagation warning. `latest_epoch` always uses the newest
epoch (and warns when that requires backward propagation), while `version_id`
forces an exact immutable version. Propagation responses include the original
TLE metadata, epoch, BSTAR (`1/earth_radius`), selection policy, warnings and
`used_version` id, making the exact element set used by SGP4 explicit.
