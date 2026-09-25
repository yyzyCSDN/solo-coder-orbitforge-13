from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class WeatherSample:
    t: float
    rain_mm_h: float
    wind_m_s: float
    cloud_fraction: float


def interpolate_weather(a: WeatherSample, b: WeatherSample, t: float):
    if not a.t <= t <= b.t:
        raise ValueError('outside weather interval')
    u = (t - a.t) / (b.t - a.t)
    return WeatherSample(
        t,
        a.rain_mm_h + u * (b.rain_mm_h - a.rain_mm_h),
        a.wind_m_s + u * (b.wind_m_s - a.wind_m_s),
        a.cloud_fraction + u * (b.cloud_fraction - a.cloud_fraction),
    )


def contact_weather_ok(sample: WeatherSample, max_rain: float, max_wind: float):
    return sample.rain_mm_h <= max_rain and sample.wind_m_s <= max_wind


def optical_weather_score(sample: WeatherSample):
    rain_penalty = min(1.0, sample.rain_mm_h / 5.0)
    cloud_penalty = min(1.0, sample.cloud_fraction)
    wind_penalty = min(1.0, sample.wind_m_s / 25.0)
    return max(0.0, 1.0 - 0.5 * cloud_penalty - 0.3 * rain_penalty - 0.2 * wind_penalty)
