from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import urlopen

from .model import (
    SGP4_MODEL,
    STALE_TLE_DAYS,
    SGP4UnavailableError,
    TLEPropagationError,
    TLEVersion,
    VersionSelection,
    parse_tle_text,
)


def sgp4_available() -> bool:
    try:
        import sgp4.api  # noqa: F401
    except Exception:
        return False
    return True


def _load_sgp4():
    try:
        from sgp4.api import WGS72, Satrec
        from sgp4.ext import jday
    except Exception as exc:
        raise SGP4UnavailableError(
            'real SGP4 support requires the official Python "sgp4>=2.21" package; '
            'the two-body/J2 propagators are intentionally not used as a substitute'
        ) from exc
    return Satrec, WGS72, jday


def _julian_date(jday, when_unix: float) -> tuple[float, float]:
    dt = datetime.fromtimestamp(when_unix, timezone.utc)
    second = dt.second + dt.microsecond / 1_000_000.0
    return jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, second)


class TLECatalog:
    """In-memory, append-only catalog keyed by NORAD satellite number.

    Every distinct raw TLE line pair is retained as a version. Repeated updates
    across day/year boundaries sort by the actual TLE epoch rather than arrival
    order.
    """

    def __init__(self, stale_after_days: float = STALE_TLE_DAYS):
        self.stale_after_days = stale_after_days
        self._versions: dict[int, dict[str, TLEVersion]] = {}

    def add(self, version: TLEVersion) -> bool:
        bucket = self._versions.setdefault(version.satellite_number, {})
        if version.version_id in bucket:
            return False
        bucket[version.version_id] = version
        return True

    def _validate_version(self, version: TLEVersion) -> None:
        Satrec, WGS72, _ = _load_sgp4()
        try:
            satrec = Satrec.twoline2rv(version.line1, version.line2, WGS72)
            if getattr(satrec, 'error', 0) != 0:
                message = getattr(satrec, 'error_message', f'SGP4 error {satrec.error}')
                raise ValueError(message)
        except SGP4UnavailableError:
            raise
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError(f'SGP4 rejected TLE {version.version_id}: {exc}') from exc

    def add_validated(self, version: TLEVersion) -> bool:
        """Add a version after constructing it with the real SGP4 parser."""
        self._validate_version(version)
        return self.add(version)

    def ingest_text(self, text: str) -> dict[str, Any]:
        parsed_pairs, errors = parse_tle_text(text)
        parsed_versions = [version for version, _ in parsed_pairs]
        accepted = 0
        duplicates = 0
        rejected_errors = list(errors)
        satellite_numbers: set[int] = set()
        for version in parsed_versions:
            satellite_numbers.add(version.satellite_number)
            if self.add(version):
                accepted += 1
            else:
                duplicates += 1
        return {
            'accepted': accepted,
            'duplicate_versions': duplicates,
            'rejected': len(rejected_errors),
            'satellite_numbers': sorted(satellite_numbers),
            'errors': rejected_errors,
        }

    def has_satellite(self, satellite_number: int) -> bool:
        return satellite_number in self._versions and bool(self._versions[satellite_number])

    def versions(self, satellite_number: int) -> list[TLEVersion]:
        if not self.has_satellite(satellite_number):
            raise KeyError(f'unknown satellite {satellite_number}')
        return sorted(self._versions[satellite_number].values(), key=lambda item: item.epoch_unix)

    def satellites(self) -> list[dict[str, Any]]:
        result = []
        now = datetime.now(timezone.utc).timestamp()
        for satnum in sorted(self._versions):
            versions = self.versions(satnum)
            latest = versions[-1]
            result.append({
                'satellite_number': satnum,
                'name': latest.name,
                'version_count': len(versions),
                'latest_version_id': latest.version_id,
                'latest_epoch_unix': latest.epoch_unix,
                'latest_epoch_utc': datetime.fromtimestamp(latest.epoch_unix, timezone.utc).isoformat(),
                'latest_bstar': latest.bstar,
                'latest_is_stale_now': latest.is_stale_at(now, self.stale_after_days),
            })
        return result

    def get_version(self, satellite_number: int, version_id: str) -> TLEVersion:
        try:
            return self._versions[satellite_number][version_id]
        except KeyError as exc:
            raise KeyError(f'unknown TLE version {version_id} for satellite {satellite_number}') from exc

    def latest_version(self, satellite_number: int) -> TLEVersion:
        return self.versions(satellite_number)[-1]

    def select(
        self,
        satellite_number: int,
        when_unix: float,
        policy: str = 'as-of',
        version_id: str | None = None,
    ) -> VersionSelection:
        versions = self.versions(satellite_number)
        warnings: list[str] = []
        if version_id is not None:
            selected = self.get_version(satellite_number, version_id)
            policy = 'explicit_version'
        elif policy == 'latest_epoch':
            selected = versions[-1]
        elif policy == 'as-of':
            not_after = [item for item in versions if item.epoch_unix <= when_unix]
            if not_after:
                selected = not_after[-1]
            else:
                selected = versions[0]
                warnings.append(
                    'requested_time_before_earliest_epoch:propagating_forward_from_earliest_version'
                )
        else:
            raise ValueError("policy must be 'as-of', 'latest_epoch', or supply version_id")

        elapsed = when_unix - selected.epoch_unix
        stale = selected.is_stale_at(when_unix, self.stale_after_days)
        if stale:
            warnings.append(
                f'selected_epoch_older_than_{self.stale_after_days:g}_days:raw_version_retained'
            )
        if policy == 'as-of' and len(versions) > 1 and any(item.epoch_unix > when_unix for item in versions):
            warnings.append('newer_epochs_exist_but_were_not_used_for_as_of_query')
        if policy in ('as-of', 'latest_epoch') and selected.epoch_unix > when_unix:
            warnings.append('selected_epoch_is_after_requested_time:propagating_backward')
        return VersionSelection(
            version=selected,
            policy=policy,
            query_unix=when_unix,
            warnings=tuple(warnings),
            elapsed_from_epoch_s=elapsed,
            stale=stale,
        )

    def propagate(
        self,
        satellite_number: int,
        when_unix: float,
        policy: str = 'as-of',
        version_id: str | None = None,
    ) -> dict[str, Any]:
        selection = self.select(satellite_number, when_unix, policy, version_id)
        Satrec, WGS72, jday = _load_sgp4()
        version = selection.version
        try:
            satrec = Satrec.twoline2rv(version.line1, version.line2, WGS72)
        except Exception as exc:
            raise TLEPropagationError(f'SGP4 rejected TLE {version.version_id}: {exc}') from exc
        if getattr(satrec, 'error', 0) != 0:
            message = getattr(satrec, 'error_message', f'SGP4 error {satrec.error}')
            raise TLEPropagationError(f'SGP4 rejected TLE {version.version_id}: {message}')
        sgp4_bstar = float(satrec.bstar)
        if abs(sgp4_bstar - version.bstar) > 1e-12:
            raise TLEPropagationError(
                f'SGP4 BSTAR mismatch for {version.version_id}: '
                f'{sgp4_bstar} != {version.bstar}'
            )

        jd, fraction = _julian_date(jday, when_unix)
        try:
            error, position_km, velocity_km_s = satrec.sgp4(jd, fraction)
        except Exception as exc:
            raise TLEPropagationError(f'SGP4 propagation failed for {version.version_id}: {exc}') from exc
        if error != 0:
            raise TLEPropagationError(
                f'SGP4 propagation failed for {version.version_id} with error {error}'
            )

        return {
            'satellite_number': satellite_number,
            'query_unix': when_unix,
            'query_utc': datetime.fromtimestamp(when_unix, timezone.utc).isoformat(),
            'position_km': [float(value) for value in position_km],
            'velocity_km_s': [float(value) for value in velocity_km_s],
            'units': {'position': 'km', 'velocity': 'km/s', 'bstar': '1/earth_radius'},
            'bstar_used': version.bstar,
            'epoch_used_unix': version.epoch_unix,
            'frame': 'TEME',
            'propagator': SGP4_MODEL,
            'raw_tle': version.raw_tle,
            'three_line_tle': version.three_line_tle,
            'used_version': selection.metadata(),
        }


def load_tle_url(url: str, catalog: TLECatalog, timeout: float = 20.0) -> dict[str, Any]:
    parts = urlsplit(url)
    if parts.scheme not in ('http', 'https') or not parts.netloc:
        raise ValueError('TLE source URL must be an absolute http or https URL')
    try:
        with urlopen(url, timeout=timeout) as response:  # noqa: S310 - caller supplies the catalog source
            charset = response.headers.get_content_charset() or 'utf-8'
            text = response.read().decode(charset, errors='replace')
    except URLError as exc:
        raise RuntimeError(f'failed to fetch TLE source {url}: {exc}') from exc
    result = catalog.ingest_text(text)
    result['source_url'] = url
    return result
