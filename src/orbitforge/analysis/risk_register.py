from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Risk:
    name: str
    probability: float
    consequence: float
    mitigation: str = ''

    @property
    def exposure(self):
        return self.probability * self.consequence

def rank(risks):
    return sorted(risks, key=lambda r: (-r.exposure, r.name))

def total_exposure(risks):
    return sum(r.exposure for r in risks)

def high_risks(risks, threshold):
    return [risk for risk in rank(risks) if risk.exposure >= threshold]

def mitigated(risk, probability_factor=1.0, consequence_factor=1.0):
    return Risk(risk.name, risk.probability * probability_factor, risk.consequence * consequence_factor, risk.mitigation)
