from __future__ import annotations

def acceptance_items():
    return [
        'time_scale_consistency',
        'frame_roundtrip',
        'orbit_propagation_conservation',
        'maneuver_solution_validity',
        'station_visibility_geometry',
        'eclipse_classification',
        'link_budget_units',
        'attitude_rotation_consistency',
        'conjunction_covariance_validity',
        'ephemeris_interpolation_continuity',
        'mission_window_boundary_semantics',
        'artifact_reproducibility',
    ]

def evaluate(results):
    missing = [name for name in acceptance_items() if name not in results]
    failed = [name for name in acceptance_items() if name in results and not results[name]]
    return {'missing': missing, 'failed': failed, 'accepted': not missing and not failed}

def require(results):
    report = evaluate(results)
    if not report['accepted']:
        raise ValueError(f"acceptance failed: missing={report['missing']} failed={report['failed']}")
    return report
