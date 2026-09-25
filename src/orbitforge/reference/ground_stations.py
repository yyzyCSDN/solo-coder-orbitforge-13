from __future__ import annotations
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class StationReference:
    code: str
    lat_rad: float
    lon_rad: float
    alt_km: float
    bands: tuple[str, ...]

STATIONS = {
    'GOLDSTONE': StationReference('GOLDSTONE', math.radians(35.2472), math.radians(-116.7933), 1.0, ('S','X','Ka')),
    'MADRID': StationReference('MADRID', math.radians(40.4314), math.radians(-4.2486), 0.7, ('S','X','Ka')),
    'CANBERRA': StationReference('CANBERRA', math.radians(-35.3983), math.radians(148.9819), 0.7, ('S','X','Ka')),
    'SVALBARD': StationReference('SVALBARD', math.radians(78.2298), math.radians(15.4078), 0.45, ('S','X')),
    'KIRUNA': StationReference('KIRUNA', math.radians(67.8571), math.radians(20.9643), 0.4, ('S','X')),
    'KOUROU': StationReference('KOUROU', math.radians(5.2514), math.radians(-52.8047), 0.03, ('S','X')),
    'MALINDI': StationReference('MALINDI', math.radians(-2.995), math.radians(40.194), 0.02, ('S','X')),
    'TROLL': StationReference('TROLL', math.radians(-72.0117), math.radians(2.535), 1.27, ('S','X')),
}

def station(code):
    return STATIONS[code]

def by_band(band):
    return [s for s in STATIONS.values() if band in s.bands]

def hemisphere_counts():
    north = sum(1 for s in STATIONS.values() if s.lat_rad >= 0.0)
    south = len(STATIONS) - north
    return {'north': north, 'south': south}
