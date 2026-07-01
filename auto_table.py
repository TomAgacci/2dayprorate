# auto_table.py
# Automatically generate a formatted table for any region list

from regional_simulator import simulate_region

def generate_table(regions, rent):
    print(f"\nAuto Table — Rent = ${rent}")
    print("---------------------------------------------------------------")
    print("City | Adj Base M | Maintenance | Profit | Eviction Prob")
    print("---------------------------------------------------------------")

    for city, data in regions.items():
        result = simulate_region(
            rent=rent,
            maintenance_multiplier=data["maintenance_multiplier"],
            strictness=data["strictness"]
        )
        print(f"{city} | {result['adjusted_base_maintenance']} | "
              f"{result['maintenance']} | {result['profit']} | "
              f"{result['eviction_probability']}")

if __name__ == "__main__":
    # Example usage (replace with JSON or CSV loader)
    sample_regions = {
        "Example City": {"maintenance_multiplier": 1.0, "strictness": 0.5}
    }
    generate_table(sample_regions, rent=600)
