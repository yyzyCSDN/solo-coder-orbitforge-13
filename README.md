# OrbitForge Mission Lab

OrbitForge is a Python library and small HTTP service for spacecraft mission
analysis: orbital mechanics, mission geometry and resource products.

## Quick start

```bash
python -m pip install -e '.[test]'
PYTHONPATH=src python -m pytest -q
orbitforge
```

The service listens on `127.0.0.1:8080` by default. `GET /live` and `GET /ready`
report service state, and the analysis endpoints live under `/v1/`.

## Satellite catalog & SGP4 propagation (`/v1/catalog`)

A versioned TLE catalog with genuine SGP4/SDP4 propagation.

```bash
# ingest (JSON, or text/plain with 2-line / 3-line TLE blocks)
curl -X POST localhost:8080/v1/catalog/tles -H 'content-type: text/plain' --data-binary 'ISS (ZARYA)
1 25544U 98067A   26269.39984368  .00031849  00000+0  59036-3 0  9995
2 25544  51.6292 159.1757 0007020 184.2024 175.8906 15.48664613587440
'

curl localhost:8080/v1/catalog/satellites                    # catalog summary
curl localhost:8080/v1/catalog/satellites/25544/versions     # every element set, original lines kept
curl 'localhost:8080/v1/catalog/satellites/25544/propagate?time=2026-09-26T16:00:00Z'
```

Catalog semantics:

- **Versioned, never overwritten.** Every distinct element set is stored as an
  immutable `TLEVersion` keyed by content hash. Re-ingesting identical lines is
  a duplicate no-op; an element set arriving with an older epoch
  (e.g. a stale daily drop) is kept as history and flagged `stale_on_arrival`,
  never silently promoted.
- **Ordered by TLE epoch, not arrival.** Cross-midnight and out-of-order
  updates sort correctly. Queries use as-of selection: the newest element set
  with `epoch <= t` (ties: later-ingested wins, flagged `epoch_conflict`).
  Before the earliest epoch the oldest set is used with a
  `backward_propagation` warning; beyond `stale_after_days` (default 7) a
  `stale_element_set` warning is attached.
- **Auditable propagation.** Every propagation response carries `version_used`
  (version id, epoch, BSTAR, content hash, the original TLE lines) plus
  `propagator` identification, so any state vector can be traced back to the
  exact element set that produced it.
- **Persistence.** Set `ORBITFORGE_CATALOG_JOURNAL=/path/catalog.jsonl` to
  journal every ingest; the catalog is rebuilt by replaying the journal on
  startup.

### Why SGP4 and not the two-body/J2 propagators

TLE element sets are *mean* elements in the SGP4 perturbation theory (WGS72
constants) and their BSTAR drag term is only defined inside that theory.
Running TLEs through a two-body or J2-only propagator — such as the generic
Kepler/Cowell helpers in `orbitforge.orbits` — misinterprets the elements and
drops drag entirely, producing errors that grow to hundreds of kilometres
within days. `orbitforge.catalog` therefore propagates exclusively with the
reference SGP4/SDP4 implementation (`python-sgp4`, Vallado STR#3), validated
in the test suite against the official SGP4-VER verification vectors, and
reports the model branch actually used (`SGP4` near-earth, `SDP4`
deep-space). Output states are in the TEME frame; UTC is used as the SGP4
time argument (UT1 differs by < 0.9 s, negligible for the inertial state).
