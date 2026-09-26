from __future__ import annotations

import pytest

sgp4 = pytest.importorskip('sgp4')
fastapi = pytest.importorskip('fastapi')
httpx = pytest.importorskip('httpx')
from fastapi.testclient import TestClient

from orbitforge.api.app import app, tle_catalog


TLE = """ISS (ZARYA)
1 25544U 98067A   24009.52003472  .00020315  00000-0  36715-3 0  9994
2 25544  51.6420 111.9092 0006703 142.3094 309.8853 15.50309799424905
ISS (ZARYA)
1 25544U 98067A   24010.52003472  .00020315  00000-0  36715-3 0  9996
2 25544  51.6420 112.9092 0006703 142.3094 309.8853 15.50309799425053
"""


@pytest.fixture(autouse=True)
def clean_catalog():
    tle_catalog._versions.clear()
    yield


def test_ingest_list_versions_and_propagate_identifies_used_version():
    client = TestClient(app)
    response = client.post('/v1/tle/ingest', json={'text': TLE})
    assert response.status_code == 200
    assert response.json()['accepted'] == 2

    listed = client.get('/v1/catalog/satellites/25544/versions').json()
    assert [item['epoch_day'] for item in listed['versions']] == [9.52003472, 10.52003472]
    assert all(item['raw_tle'].startswith('1 ') for item in listed['versions'])

    query = '2024-01-10T00:00:00+00:00'
    picked = client.get(
        '/v1/catalog/satellites/25544/selected-version',
        params={'time_utc': query, 'policy': 'as-of'},
    ).json()
    assert picked['selection']['epoch_day'] == 9.52003472
    assert picked['selection']['propagator'] == 'SGP4/WGS72'

    propagated = client.post(
        '/v1/tle/propagate',
        json={'satellite_number': 25544, 'time_utc': query, 'policy': 'as-of'},
    )
    assert propagated.status_code == 200
    body = propagated.json()
    assert body['frame'] == 'TEME'
    assert body['propagator'] == 'SGP4/WGS72'
    assert body['used_version']['epoch_day'] == 9.52003472
    assert body['used_version']['bstar'] == pytest.approx(0.00036715)
    day9 = listed['versions'][0]
    explicit = client.post(
        '/v1/tle/propagate',
        json={
            'satellite_number': 25544,
            'time_utc': query,
            'version_id': day9['version_id'],
        },
    ).json()
    assert explicit['used_version']['version_id'] == day9['version_id']
    assert explicit['used_version']['selection_policy'] == 'explicit_version'
    assert explicit['raw_tle'] == day9['raw_tle']


def test_duplicate_ingestion_is_idempotent_and_original_versions_remain():
    client = TestClient(app)
    first = client.post('/v1/tle/ingest', json={'text': TLE}).json()
    second = client.post('/v1/tle/ingest', json={'text': TLE}).json()
    assert first['accepted'] == 2
    assert second['accepted'] == 0
    assert second['duplicate_versions'] == 2
    assert client.get('/v1/catalog/satellites/25544/versions').json()['count'] == 2


def test_partial_bad_batch_reports_rejections():
    bad = TLE + 'BAD-SAT\n1 00000U 00000A   24010.00000000  .00000000  00000-0  00000-0 0  9990\n'
    client = TestClient(app)
    response = client.post('/v1/tle/ingest', json={'text': bad})
    assert response.status_code == 207
    assert response.json()['accepted'] == 2
    assert response.json()['rejected'] == 1
