from __future__ import annotations

from datetime import datetime, timezone

import pytest

from orbitforge.tle import TLECatalog
from orbitforge.tle.catalog import sgp4_available
from orbitforge.tle.model import TLEParseError, TLEVersion, parse_tle_text


def checksummed(line: str) -> str:
    total = 0
    for char in line[:-1]:
        if char.isdigit():
            total += int(char)
        elif char == '-':
            total += 1
    return line[:-1] + str(total % 10)


def make_tle(epoch: str, line1_checksum_placeholder: str = '0', bstar: str = ' 36715-3', rev: str = '42490') -> tuple[str, str]:
    line1 = checksummed(
        f'1 25544U 98067A   {epoch}  .00020315  00000-0 {bstar} 0  999{line1_checksum_placeholder}'
    )
    line2 = checksummed(
        f'2 25544  51.6420 111.9092 0006703 142.3094 309.8853 15.50309799{rev}5'
    )
    return line1, line2


def epoch_unix(year: int, day: float) -> float:
    return datetime(year, 1, 1, tzinfo=timezone.utc).timestamp() + (day - 1.0) * 86400.0


def test_real_tle_parser_preserves_epoch_bstar_and_raw_lines():
    l1, l2 = make_tle('24009.50000000')
    version = TLEVersion.from_lines('ISS (ZARYA)', l1, l2)
    assert version.raw_tle == l1 + '\n' + l2
    assert version.epoch_year == 2024
    assert version.epoch_day == pytest.approx(9.5)
    assert version.epoch_unix == pytest.approx(epoch_unix(2024, 9.5))
    assert version.bstar == pytest.approx(0.00036715)
    assert version.satellite_number == 25544


def test_catalog_retains_all_versions_and_sorts_cross_day_epochs():
    old = make_tle('24008.50000000')
    new = make_tle('24010.50000000')
    catalog = TLECatalog()
    assert catalog.ingest_text('\n'.join(new))['accepted'] == 1
    assert catalog.ingest_text('\n'.join(old))['accepted'] == 1
    assert catalog.ingest_text('\n'.join(new))['duplicate_versions'] == 1

    versions = catalog.versions(25544)
    assert [item.epoch_day for item in versions] == [8.5, 10.5]
    assert catalog.latest_version(25544).version_id == versions[-1].version_id


def test_catalog_sorts_epochs_across_year_boundary():
    old = TLEVersion.from_lines('', *make_tle('99364.00000000'))
    new = TLEVersion.from_lines('', *make_tle('00001.00000000'))
    assert old.epoch_year == 1999
    assert new.epoch_year == 2000
    assert new.epoch_unix > old.epoch_unix


def test_as_of_selection_identifies_which_raw_version_propagates():
    day8 = make_tle('24008.50000000')
    day10 = make_tle('24010.50000000')
    catalog = TLECatalog()
    catalog.ingest_text('\n'.join(day8 + day10))

    query = epoch_unix(2024, 9.0)
    selection = catalog.select(25544, query)
    assert selection.version.epoch_day == 8.5
    assert selection.policy == 'as-of'
    assert any('newer_epochs_exist' in warning for warning in selection.warnings)

    explicit = catalog.select(
        25544,
        query,
        version_id=TLEVersion.from_lines('', *day10).version_id,
    )
    assert explicit.policy == 'explicit_version'
    assert explicit.version.epoch_day == 10.5


def test_sgp4_propagation_uses_teme_and_bstar_not_two_body_or_j2():
    pytest.importorskip('sgp4')
    l1, l2 = make_tle('24009.52003472', bstar=' 36715-3')
    catalog = TLECatalog()
    catalog.ingest_text('ISS (ZARYA)\n' + l1 + '\n' + l2)
    at_epoch = epoch_unix(2024, 9.5)

    result = catalog.propagate(25544, at_epoch)
    assert result['propagator'] == 'SGP4/WGS72'
    assert result['frame'] == 'TEME'
    assert result['units'] == {'position': 'km', 'velocity': 'km/s', 'bstar': '1/earth_radius'}
    assert result['used_version']['bstar'] == pytest.approx(0.00036715)
    assert result['used_version']['bstar_units'] == '1/earth_radius'
    assert result['bstar_used'] == pytest.approx(0.00036715)
    assert result['epoch_used_unix'] == pytest.approx(TLEVersion.from_lines('', l1, l2).epoch_unix)
    assert result['used_version']['version_id'] == TLEVersion.from_lines('', l1, l2).version_id
    radius = sum(value * value for value in result['position_km']) ** 0.5
    assert 6700 < radius < 6900
    speed = sum(value * value for value in result['velocity_km_s']) ** 0.5
    assert 7 < speed < 8


def test_stale_root_is_retained_but_flagged():
    old = make_tle('24001.00000000')
    catalog = TLECatalog(stale_after_days=14)
    catalog.ingest_text('\n'.join(old))
    selection = catalog.select(25544, epoch_unix(2024, 20.0))
    assert selection.stale is True
    assert any('older_than_14_days' in warning for warning in selection.warnings)
    assert len(catalog.versions(25544)) == 1


def test_bad_checksum_is_rejected_without_fallback():
    l1, l2 = make_tle('24009.50000000')
    bad_l2 = l2[:-1] + str((int(l2[-1]) + 1) % 10)
    with pytest.raises(TLEParseError, match='checksum'):
        TLEVersion.from_lines('ISS', l1, bad_l2)
    parsed_versions, errors = parse_tle_text(l1 + '\n' + bad_l2)
    assert parsed_versions == []
    assert errors and errors[0]['message'].startswith('TLE line 2 checksum')


def test_sgp4_runtime_is_real():
    sgp4 = pytest.importorskip('sgp4')
    assert sgp4_available() is True
    assert hasattr(sgp4, 'api')
