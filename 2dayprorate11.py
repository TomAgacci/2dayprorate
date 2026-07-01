#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Regional Rent + Maintenance + Eviction Simulator
# GitHub-ready module for 2dayprorate
#
# This file intentionally contains NO hard-coded cities.
# You can plug in any region list and multipliers externally.

import math

# ---------------------------------------------------------
# Core constants (override as needed)
# ---------------------------------------------------------
BASE_MAINTENANCE = 30.0
TAMA_FACTOR = math.pi**2 / 6      # ≈ 1.644934
RESIDUAL_INCOME = 2830 - (800 + 200)   # Your model: income - essentials - liabilities

# ---------------------------------------------------------
# Maintenance collapse
# ---------------------------------------------------------
def maintenance_collapse(base_maintenance: float) -> float:
    """
    Collapsed maintenance using your Tama factor.
    Labeled simply as 'maintenance' for table output.
    """
    return base_maintenance * TAMA_FACTOR

# ---------------------------------------------------------
# Eviction probability model
# ---------------------------------------------------------
def eviction_probability(rent: float, strictness: float) -> float:
    """
    Eviction probability based on:
    - Rent burden
    - Base eviction probability
    - Regional strictness multiplier
    """
    burden = rent / RESIDUAL_INCOME
    p_base = 0.34 + 0.08 * burden
    p = p_base * (1 + strictness / 10)
    return round(p, 4)

# ---------------------------------------------------------
# Region simulation
# ---------------------------------------------------------
def simulate_region(
    rent: float,
    maintenance_multiplier: float,
    strictness: float
):
    """
    Compute:
    - Adjusted base maintenance
    - Collapsed maintenance
    - Profit
    - Eviction probability
    """
    adjusted_base = BASE_MAINTENANCE * maintenance_multiplier
    maintenance = maintenance_collapse(adjusted_base)
    profit = rent - maintenance
    eviction = eviction_probability(rent, strictness)

    return {
        "rent": round(rent, 2),
        "adjusted_base_maintenance": round(adjusted_base, 2),
        "maintenance": round(maintenance, 2),
        "profit": round(profit, 2),
        "eviction_probability": eviction
    }

# ---------------------------------------------------------
# Example usage (safe to remove or replace)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Example region input (replace with your actual region list)
    regions = {
        "ExampleRegion": {
            "maintenance_multiplier": 1.00,
            "strictness": 0.50
        }
    }

    rent_value = 600  # Example rent

    print("\nRegional Rent Simulator\n------------------------")
    for region, data in regions.items():
        result = simulate_region(
            rent=rent_value,
            maintenance_multiplier=data["maintenance_multiplier"],
            strictness=data["strictness"]
        )
        print(f"{region}: {result}")
