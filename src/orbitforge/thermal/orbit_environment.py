from __future__ import annotations
from orbitforge.environment.albedo import albedo_flux_w_m2, earth_ir_flux_w_m2
from orbitforge.core.constants import SOLAR_CONSTANT_W_M2


def external_fluxes(alt_km, eclipse_state, sun_incidence_cos, earth_view_cos=1.0):
    direct = 0.0 if eclipse_state == 'umbra' else SOLAR_CONSTANT_W_M2 * max(0.0, sun_incidence_cos)
    albedo = 0.0 if eclipse_state == 'umbra' else albedo_flux_w_m2(alt_km, 1.0) * max(0.0, earth_view_cos)
    earth_ir = earth_ir_flux_w_m2(alt_km) * max(0.0, earth_view_cos)
    return {'solar_w_m2': direct, 'albedo_w_m2': albedo, 'earth_ir_w_m2': earth_ir}


def absorbed_power(area_m2, absorptivity, ir_emissivity, fluxes):
    shortwave = fluxes['solar_w_m2'] + fluxes['albedo_w_m2']
    return area_m2 * (absorptivity * shortwave + ir_emissivity * fluxes['earth_ir_w_m2'])


def orbit_average_flux(samples):
    if not samples:
        return {'solar_w_m2': 0.0, 'albedo_w_m2': 0.0, 'earth_ir_w_m2': 0.0}
    return {key: sum(s[key] for s in samples) / len(samples) for key in samples[0]}
