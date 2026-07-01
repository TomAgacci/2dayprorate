#!/usr/bin/env python3
# simulator.py
# Multi-region rent, maintenance, profit, and eviction simulator

import math
import csv
from regions import REGIONS

# ---------------------------------------------------------
# Core constants
# ---------------------------------------------------------
BASE_MAINTENANCE = 30.0
TAMA_FACTOR = math.pi**2 / 6
RESIDUAL_INCOME = 2830 - (800 + 200)  # income - essentials - liabilities

# ---------------------------------------------------------
# Maintenance collapse
# ---------------------------------------------------------
def maintenance_collapse(base_maintenance: float) -> float:
    return base_maintenance * TAMA_FACTOR

# ---------------------------------------------------------
# Eviction probability
# ---------------------------------------------------------
def eviction_probability(rent: float, strictness: float) -> float:
    burden = rent / RESIDUAL_INCOME
    p_base = 0.34 + 0.08 * burden
    p = p_base * (1 + strictness / 10)
    return round(p, 4)

# ---------------------------------------------------------
# Region simulation
# ---------------------------------------------------------
def simulate_region(rent: float, maintenance_multiplier: float, strictness: float):
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
# Print table
# ---------------------------------------------------------
def print_table(rent: float):
    print(f"\nRegional Simulation — Rent = ${rent}")
    print("---------------------------------------------------------------")
    print("City | Adj Base M | Maintenance | Profit | Eviction Prob")
    print("---------------------------------------------------------------")

    for city, data in REGIONS.items():
        result = simulate_region(
            rent=rent,
            maintenance_multiplier=data["maintenance_multiplier"],
            strictness=data["strictness"]
        )
        print(f"{city} | {result['adjusted_base_maintenance']} | "
              f"{result['maintenance']} | {result['profit']} | "
              f"{result['eviction_probability']}")

# ---------------------------------------------------------
# Optional CSV export
# ---------------------------------------------------------
def export_csv(rent: float, filename="regional_output.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "City", "Rent", "Adjusted Base Maintenance",
            "Maintenance", "Profit", "Eviction Probability"
        ])

        for city, data in REGIONS.items():
            result = simulate_region(
                rent=rent,
                maintenance_multiplier=data["maintenance_multiplier"],
                strictness=data["strictness"]
            )
            writer.writerow([
                city,
                result["rent"],
                result["adjusted_base_maintenance"],
                result["maintenance"],
                result["profit"],
                result["eviction_probability"]
            ])

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
if __name__ == "__main__":
    rent_value = 600  # default
    print_table(rent_value)
    # export_csv(rent_value)  # uncomment to export CSV
