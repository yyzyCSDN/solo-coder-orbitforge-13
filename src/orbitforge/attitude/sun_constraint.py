from __future__ import annotations
import math

def keepout_ok(boresight, sun_direction, min_angle_rad):
    return boresight.unit().angle(sun_direction.unit()) >= min_angle_rad

def limb_keepout(position, target_direction, earth_radius_km=6378.137, margin_rad=0.0):
    nadir = (position * -1).unit()
    limb = math.asin(min(1, earth_radius_km / position.norm()))
    return nadir.angle(target_direction.unit()) >= limb + margin_rad
