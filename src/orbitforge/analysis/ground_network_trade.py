from __future__ import annotations

def evaluate_network(network, demand_mb_day, cost_weight=1.0, availability_weight=100.0):
    capacity = sum(station.get('capacity_mb_day', 0.0) for station in network)
    cost = sum(station.get('annual_cost', 0.0) for station in network)
    all_down = 1.0
    for station in network:
        all_down *= 1.0 - station.get('availability', 1.0)
    availability = 1.0 - all_down
    deficit = max(0.0, demand_mb_day - capacity)
    score = availability_weight * availability - cost_weight * cost - 10.0 * deficit
    return {
        'capacity_mb_day': capacity,
        'annual_cost': cost,
        'availability': availability,
        'deficit_mb_day': deficit,
        'score': score,
    }

def compare_networks(networks, demand_mb_day):
    rows = []
    for name, stations in networks.items():
        row = evaluate_network(stations, demand_mb_day)
        row['name'] = name
        rows.append(row)
    return sorted(rows, key=lambda row: row['score'], reverse=True)
