from __future__ import annotations
import random
from orbitforge.core.vector import Vec3

def gyro_measurement(true_rate: Vec3, bias: Vec3, noise_sigma: float, rng: random.Random):
    return Vec3(true_rate.x + bias.x + rng.gauss(0.0, noise_sigma), true_rate.y + bias.y + rng.gauss(0.0, noise_sigma), true_rate.z + bias.z + rng.gauss(0.0, noise_sigma))

def star_tracker_noise(vector: Vec3, sigma_rad: float, rng: random.Random):
    perturb = Vec3(rng.gauss(0.0, sigma_rad), rng.gauss(0.0, sigma_rad), rng.gauss(0.0, sigma_rad))
    return (vector.unit() + perturb).unit()

def bias_random_walk(bias: Vec3, sigma_per_sqrt_s: float, dt_s: float, rng: random.Random):
    scale = sigma_per_sqrt_s * dt_s ** 0.5
    return Vec3(bias.x + rng.gauss(0.0, scale), bias.y + rng.gauss(0.0, scale), bias.z + rng.gauss(0.0, scale))
