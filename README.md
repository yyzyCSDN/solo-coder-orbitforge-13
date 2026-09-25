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
