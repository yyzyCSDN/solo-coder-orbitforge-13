import datetime as dt
import math

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from orbitforge.io.tle import parse, epoch_datetime, checksum_ok, _implied_decimal
from orbitforge.catalog import CatalogStore, SGP4Propagator, UnknownSatelliteError
from orbitforge.catalog.service import build_router

UTC = dt.timezone.utc

# Official SGP4 verification TLE (Vallado et al., "Revisiting Spacetrack
# Report #3", SGP4-VER.TLE), satellite 00005 — checksums valid as published.
VANGUARD_L1 = '1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753'
VANGUARD_L2 = '2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667'
# Reference state at the TLE epoch (tsince = 0), from the STR#3 verification file.
VANGUARD_R_KM = (7022.46529266, -1400.08296755, 0.03995155)
VANGUARD_V_KM_S = (1.893841015, 6.405893759, 4.534807250)

# ISS-derived element sets (realistic 2024-09-12/13 values). Checksums are
# recomputed by _fix() so the fixtures stay self-consistent after splicing.
ISS_L1 = '1 25544U 98067A   24256.99652778  .00016717  00000-0  31257-3 0  9990'
ISS_L2 = '2 25544  51.6416 208.9163 0006703  69.9862  25.2906 15.49560532469940'

# Synthetic GEO bird, period > 225 min forces the deep-space SDP4 branch.
GEO_L1 = '1 40900U 15048A   24256.50000000 -.00000034  00000-0  00000-0 0  0000'
GEO_L2 = '2 40900   0.0500  10.0000 0002000 100.0000 250.0000  1.00270000  1000'

# Exact epochs of the ISS element sets, computed the same way epoch_datetime()
# does, so equality assertions are not fooled by the TLE's 1e-8-day quantum.
ISS_V1_EPOCH = dt.datetime(2024, 1, 1, tzinfo=UTC) + dt.timedelta(days=256.99652778 - 1.0)
ISS_V2_EPOCH = dt.datetime(2024, 1, 1, tzinfo=UTC) + dt.timedelta(days=257.01041667 - 1.0)


def _fix(prefix: str) -> str:
    """Append a valid TLE checksum to a 68-char prefix."""
    assert len(prefix) == 68, f'bad prefix length {len(prefix)}: {prefix!r}'
    total = sum(int(c) if c.isdigit() else 1 if c == '-' else 0 for c in prefix)
    return prefix + str(total % 10)


def _tle(line1_prefix: str, line2_prefix: str) -> tuple[str, str]:
    return _fix(line1_prefix), _fix(line2_prefix)


def _with_epoch(line1: str, epoch_field: str, elset: str) -> str:
    """Splice a new epoch (YYDDD.DDDDDDDD) and element-set number into line 1."""
    assert len(epoch_field) == 14
    return line1[:18] + epoch_field + line1[32:64] + elset.rjust(4) + line1[68]


def _with_bstar(line1: str, bstar_field: str) -> str:
    """Splice a new BSTAR field (8 chars, e.g. ' 31257-3') into line 1."""
    assert len(bstar_field) == 8
    return line1[:53] + bstar_field + line1[61:]


# ISS versions used across the tests:
#   stale:  epoch 2024-08-28 12:00 (day 241), elset 980
#   v1:     epoch 2024-09-12 23:55 (day 256, late evening), elset 999
#   v2:     epoch 2024-09-13 00:15 (day 257, just after midnight), elset 1000
ISS_STALE = _tle(_with_epoch(ISS_L1, '24241.50000000', ' 980')[:68], ISS_L2[:68])
ISS_V1 = _tle(ISS_L1[:68], ISS_L2[:68])
ISS_V2 = _tle(_with_epoch(ISS_L1, '24257.01041667', '1000')[:68], ISS_L2[:68])
GEO = _tle(GEO_L1[:68], GEO_L2[:68])


def make_client(store=None):
    app = FastAPI()
    app.include_router(build_router(store or CatalogStore()))
    return TestClient(app)


# -- TLE parsing ---------------------------------------------------------

def test_parse_official_tle_fields():
    rec = parse('VANGUARD 1', VANGUARD_L1, VANGUARD_L2)
    assert rec.satellite_number == 5
    assert (rec.epoch_year, rec.epoch_day) == (2000, 179.78495062)
    assert rec.bstar_inv_earth_radii == pytest.approx(2.8098e-5)
    assert rec.mean_motion_rev_day == pytest.approx(10.82419157)
    assert math.degrees(rec.inclination_rad) == pytest.approx(34.2682)
    assert rec.element_set_number == 475
    expected = dt.datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)
    assert abs(epoch_datetime(rec) - expected) < dt.timedelta(milliseconds=1)


def test_official_tle_checksums_are_valid():
    assert checksum_ok(VANGUARD_L1) and checksum_ok(VANGUARD_L2)


def test_checksum_mismatch_rejected():
    bad = VANGUARD_L1[:30] + '9' + VANGUARD_L1[31:]
    with pytest.raises(ValueError, match='checksum'):
        parse('', bad, VANGUARD_L2)


def test_satellite_number_mismatch_rejected():
    other = _fix('2 00006  34.2682 348.7242 1859667 331.7664  19.3264 10.8241915741366')
    with pytest.raises(ValueError, match='disagree'):
        parse('', VANGUARD_L1, other)


def test_implied_decimal_fields():
    assert _implied_decimal(' 28098-4') == pytest.approx(2.8098e-5)
    assert _implied_decimal('-11606-4') == pytest.approx(-1.1606e-5)
    assert _implied_decimal(' 00000-0') == 0.0
    assert _implied_decimal('        ') == 0.0


# -- catalog store -------------------------------------------------------

def test_ingest_dedupes_identical_tle():
    store = CatalogStore()
    r1 = store.ingest('ISS', *ISS_V1)
    r2 = store.ingest('ISS', *ISS_V1)
    assert r1.created and not r2.created
    assert r1.version.version_id == r2.version.version_id
    assert len(store.versions(25544)) == 1


def test_versions_sorted_by_epoch_not_arrival():
    store = CatalogStore()
    store.ingest('ISS', *ISS_V2)     # newer arrives first (cross-day drop)
    store.ingest('ISS', *ISS_V1)
    store.ingest('ISS', *ISS_STALE)  # stale element set arrives last
    epochs = [v.epoch for v in store.versions(25544)]
    assert epochs == sorted(epochs)
    assert store.latest(25544).epoch == ISS_V2_EPOCH


def test_stale_tle_kept_as_history_not_used():
    store = CatalogStore()
    v2 = store.ingest('ISS', *ISS_V2).version
    res = store.ingest('ISS', *ISS_STALE)
    assert res.created
    assert any('stale_on_arrival' in w for w in res.warnings)
    assert store.latest(25544).version_id == v2.version_id
    sel = store.select(25544, dt.datetime(2024, 9, 13, 12, 0, tzinfo=UTC))
    assert sel.version.version_id == v2.version_id
    assert len(store.versions(25544)) == 2  # original stale set preserved


def test_epoch_conflict_last_writer_wins():
    store = CatalogStore()
    store.ingest('ISS', *ISS_V1)
    conflicting = _tle(_with_bstar(ISS_L1, ' 20000-3')[:68], ISS_L2[:68])
    res = store.ingest('ISS', *conflicting)  # same epoch, different drag term
    assert any('epoch_conflict' in w for w in res.warnings)
    assert len(store.versions(25544)) == 2
    sel = store.select(25544, dt.datetime(2024, 9, 13, 0, 0, tzinfo=UTC))
    assert sel.version.version_id == res.version.version_id


def test_select_as_of_and_backward():
    store = CatalogStore()
    store.ingest('ISS', *ISS_V1)
    store.ingest('ISS', *ISS_V2)
    before = store.select(25544, dt.datetime(2024, 9, 12, 23, 0, tzinfo=UTC))
    assert before.backward and before.age_days < 0
    between = store.select(25544, dt.datetime(2024, 9, 13, 0, 5, tzinfo=UTC))
    assert not between.backward and between.version.epoch == ISS_V1_EPOCH
    after = store.select(25544, dt.datetime(2024, 9, 13, 1, 0, tzinfo=UTC))
    assert after.version.epoch == ISS_V2_EPOCH


def test_journal_persistence_across_restart(tmp_path):
    journal = tmp_path / 'catalog.jsonl'
    with CatalogStore(journal_path=str(journal)) as store:
        store.ingest('ISS', *ISS_V1, source='celestrak')
        store.ingest('ISS', *ISS_V2)
    with CatalogStore(journal_path=str(journal)) as reopened:
        versions = reopened.versions(25544)
        assert len(versions) == 2
        assert versions[0].line1 == ISS_V1[0] and versions[0].line2 == ISS_V1[1]
        assert versions[0].source == 'celestrak'
        again = reopened.ingest('ISS', *ISS_V1)
        assert not again.created  # duplicates still suppressed after reload


def test_unknown_satellite_raises():
    with pytest.raises(UnknownSatelliteError):
        CatalogStore().versions(99999)


# -- genuine SGP4 propagation ---------------------------------------------

def test_sgp4_matches_vallado_verification_vector():
    """Anchors the propagator to the official STR#3 reference output."""
    store = CatalogStore()
    version = store.ingest('VANGUARD 1', VANGUARD_L1, VANGUARD_L2).version
    result = SGP4Propagator().propagate(version, version.epoch)
    assert result.sgp4_error == 0
    assert result.model == 'SGP4'
    for got, want in zip(result.position_km, VANGUARD_R_KM):
        assert got == pytest.approx(want, abs=1e-6)
    for got, want in zip(result.velocity_km_s, VANGUARD_V_KM_S):
        assert got == pytest.approx(want, abs=1e-9)


def test_bstar_drag_actually_applied():
    """Zeroing BSTAR must change the trajectory — proof the drag term is
    modeled (a two-body/J2 propagator would ignore BSTAR entirely)."""
    store = CatalogStore()
    real = store.ingest('ISS', *ISS_V1).version
    zeroed = store.ingest('ISS', *_tle(_with_bstar(ISS_L1, ' 00000-0')[:68], ISS_L2[:68])).version
    prop = SGP4Propagator()
    when = real.epoch + dt.timedelta(days=1)
    r_real = prop.propagate(real, when).position_km
    r_zero = prop.propagate(zeroed, when).position_km
    separation = math.dist(r_real, r_zero)
    assert separation > 1.0  # km after one day of ISS drag


def test_deep_space_uses_sdp4_branch():
    store = CatalogStore()
    version = store.ingest('GEO', *GEO).version
    result = SGP4Propagator().propagate(version, version.epoch + dt.timedelta(hours=6))
    assert result.model == 'SDP4'
    radius = math.dist(result.position_km, (0, 0, 0))
    assert 41000 < radius < 43000  # km, geosynchronous radius


def test_propagation_result_names_version_used():
    store = CatalogStore()
    store.ingest('ISS', *ISS_V1)
    v2 = store.ingest('ISS', *ISS_V2).version
    prop = SGP4Propagator()
    when = dt.datetime(2024, 9, 13, 1, 0, tzinfo=UTC)
    result = prop.propagate(store.select(25544, when).version, when)
    assert result.version.version_id == v2.version_id
    assert result.minutes_from_epoch == pytest.approx(45.0)


# -- HTTP service ---------------------------------------------------------

def test_api_ingest_json_and_text_plain():
    client = make_client()
    r = client.post('/v1/catalog/tles', json={
        'source': 'celestrak',
        'tles': [{'name': 'ISS', 'line1': ISS_V1[0], 'line2': ISS_V1[1]}]})
    assert r.status_code == 200
    assert r.json()['ingested'] == 1
    text = f'ISS (ZARYA)\n{ISS_V2[0]}\n{ISS_V2[1]}\n'
    r = client.post('/v1/catalog/tles', content=text,
                    headers={'content-type': 'text/plain'})
    assert r.json()['ingested'] == 1
    again = client.post('/v1/catalog/tles', content=text,
                        headers={'content-type': 'text/plain'})
    assert again.json()['duplicates'] == 1  # same TLE not re-versioned


def test_api_versions_preserve_originals():
    client = make_client()
    client.post('/v1/catalog/tles', json={'tles': [
        {'name': 'ISS', 'line1': ISS_V2[0], 'line2': ISS_V2[1]},
        {'name': 'ISS', 'line1': ISS_V1[0], 'line2': ISS_V1[1]},
        {'name': 'ISS', 'line1': ISS_STALE[0], 'line2': ISS_STALE[1]},
    ]})
    r = client.get('/v1/catalog/satellites/25544/versions')
    versions = r.json()['versions']
    assert len(versions) == 3
    assert [v['line1'] for v in versions] == [ISS_STALE[0], ISS_V1[0], ISS_V2[0]]
    assert versions[-1]['is_latest'] and not versions[0]['is_latest']
    assert all(v['content_hash'] and v['epoch'] for v in versions)


def test_api_propagate_identifies_version_used_across_midnight():
    client = make_client()
    client.post('/v1/catalog/tles', json={'tles': [
        {'name': 'ISS', 'line1': ISS_V1[0], 'line2': ISS_V1[1]},
        {'name': 'ISS', 'line1': ISS_V2[0], 'line2': ISS_V2[1]},
    ]})
    # 00:05 on the 13th: the 00:15 update is not yet valid -> v1 must be used
    r = client.get('/v1/catalog/satellites/25544/propagate',
                   params={'time': '2024-09-13T00:05:00Z'})
    body = r.json()
    used_epoch = dt.datetime.fromisoformat(body['version_used']['epoch'].replace('Z', '+00:00'))
    assert used_epoch == ISS_V1_EPOCH
    assert body['propagator']['name'] == 'SGP4'
    assert body['propagator']['library'] == 'python-sgp4'
    assert body['frame'] == 'TEME'
    # 01:00: the post-midnight update takes over
    r = client.get('/v1/catalog/satellites/25544/propagate',
                   params={'time': '2024-09-13T01:00:00Z'})
    body = r.json()
    used_epoch = dt.datetime.fromisoformat(body['version_used']['epoch'].replace('Z', '+00:00'))
    assert used_epoch == ISS_V2_EPOCH
    assert body['minutes_from_epoch'] == pytest.approx(45.0)


def test_api_propagate_matches_vallado_vector_through_http():
    client = make_client()
    client.post('/v1/catalog/tles', json={'tles': [
        {'name': 'VANGUARD 1', 'line1': VANGUARD_L1, 'line2': VANGUARD_L2}]})
    r = client.get('/v1/catalog/satellites/5/propagate',
                   params={'time': '2000-06-27T18:50:19.733568Z'})
    assert r.status_code == 200
    pos = r.json()['position_km']
    for got, want in zip(pos, VANGUARD_R_KM):
        assert got == pytest.approx(want, abs=1e-4)


def test_api_stale_and_backward_warnings():
    client = make_client()
    client.post('/v1/catalog/tles', json={'tles': [
        {'name': 'ISS', 'line1': ISS_V1[0], 'line2': ISS_V1[1]}]})
    r = client.get('/v1/catalog/satellites/25544/propagate',
                   params={'time': '2024-10-13T00:00:00Z'})
    assert any('stale_element_set' in w for w in r.json()['warnings'])
    r = client.get('/v1/catalog/satellites/25544/propagate',
                   params={'time': '2024-09-12T00:00:00Z'})
    assert any('backward_propagation' in w for w in r.json()['warnings'])


def test_api_unknown_satellite_404():
    assert make_client().get('/v1/catalog/satellites/99999/propagate',
                             params={'time': '2024-09-13T00:00:00Z'}).status_code == 404


def test_api_bad_tle_rejected_not_stored():
    client = make_client()
    bad = ISS_V1[0][:30] + '9' + ISS_V1[0][31:]
    r = client.post('/v1/catalog/tles', json={'tles': [
        {'name': 'ISS', 'line1': bad, 'line2': ISS_V1[1]}]})
    assert r.json()['ingested'] == 0
    assert 'error' in r.json()['results'][0]
    assert client.get('/v1/catalog/satellites/25544').status_code == 404


def test_api_batch_propagate():
    client = make_client()
    client.post('/v1/catalog/tles', json={'tles': [
        {'name': 'ISS', 'line1': ISS_V1[0], 'line2': ISS_V1[1]}]})
    r = client.post('/v1/catalog/satellites/25544/propagate', json={
        'times': ['2024-09-13T00:00:00Z', '2024-09-13T00:10:00Z']})
    states = r.json()['states']
    assert len(states) == 2
    assert states[0]['minutes_from_epoch'] == pytest.approx(5.0)
    assert states[1]['minutes_from_epoch'] == pytest.approx(15.0)


def test_api_propagator_info_is_honest_about_engine():
    client = make_client()
    info = client.get('/v1/catalog/propagator').json()
    assert info['name'] == 'SGP4'
    assert info['library'] == 'python-sgp4'
    assert info['output_frame'] == 'TEME'
