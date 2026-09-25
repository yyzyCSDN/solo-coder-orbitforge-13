from __future__ import annotations
import math


def rms_jitter(samples_rad):
    if not samples_rad:
        return 0.0
    mean = sum(samples_rad) / len(samples_rad)
    return math.sqrt(sum((x - mean) ** 2 for x in samples_rad) / len(samples_rad))

def smear_pixels(jitter_rad, focal_length_mm, pixel_pitch_um):
    displacement_mm = focal_length_mm * math.tan(jitter_rad)
    return displacement_mm * 1000.0 / pixel_pitch_um

def meets_imaging_limit(samples_rad, focal_length_mm, pixel_pitch_um, max_smear_pixels):
    return smear_pixels(rms_jitter(samples_rad), focal_length_mm, pixel_pitch_um) <= max_smear_pixels
