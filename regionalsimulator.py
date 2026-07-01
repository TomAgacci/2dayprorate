#!/usr/bin/env python3
# regional_simulator.py
# Blank multi-region rent, maintenance, profit, and eviction simulator
# Ready for GitHub: 2dayprorate project

import math

# ---------------------------------------------------------
# Core constants (override as needed)
# ---------------------------------------------------------
BASE_MAINTENANCE = 30.0
TAMA_FACTOR = math.pi**2 / 6          # ≈ 1.644934
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
# Main interactive loop
# ---------------------------------------------------------
def main():
    print("\nBlank Regional Simulator")
    print("------------------------")

    rent_value = float(input("Enter monthly rent: "))

    regions = {}

    print("\nEnter regions (type 'done' to finish):")
    while True:
        name = input("Region name: ")
        if name.lower() == "done":
            break

        maintenance_multiplier = float(input("  Maintenance multiplier: "))
        strictness = float(input("  Strictness (0.0–1.0 typical): "))

        regions[name] = {
            "maintenance_multiplier": maintenance_multiplier,
            "strictness": strictness
        }

    print("\nSimulation Results")
    print("---------------------------------------------------------------")
    print("Region | Adj Base M | Maintenance | Profit | Eviction Prob")
    print("---------------------------------------------------------------")

    for region, data in regions.items():
        result = simulate_region(
            rent=rent_value,
            maintenance_multiplier=data["maintenance_multiplier"],
            strictness=data["strictness"]
        )
        print(f"{region} | {result['adjusted_base_maintenance']} | "
              f"{result['maintenance']} | {result['profit']} | "
              f"{result['eviction_probability']}")

# ---------------------------------------------------------
# Run
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
