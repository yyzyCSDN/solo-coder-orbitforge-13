from __future__ import annotations
import math

def rms(values):
    return math.sqrt(sum(v * v for v in values) / len(values)) if values else 0.0

def chi_square(residuals, sigmas):
    if len(residuals) != len(sigmas):
        raise ValueError('residual and sigma lengths differ')
    return sum((r / s) ** 2 for r, s in zip(residuals, sigmas) if s > 0.0)

def reduced_chi_square(residuals, sigmas, parameter_count):
    dof = len(residuals) - parameter_count
    if dof <= 0:
        raise ValueError('nonpositive degrees of freedom')
    return chi_square(residuals, sigmas) / dof

def residual_summary(residuals):
    if not residuals:
        return {'count': 0, 'rms': 0.0, 'mean': 0.0, 'max_abs': 0.0}
    return {
        'count': len(residuals),
        'rms': rms(residuals),
        'mean': sum(residuals) / len(residuals),
        'max_abs': max(abs(v) for v in residuals),
    }

def passes_quality_gate(residuals, max_rms, max_abs):
    summary = residual_summary(residuals)
    return summary['rms'] <= max_rms and summary['max_abs'] <= max_abs
