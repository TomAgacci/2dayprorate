# csv_loader.py
# Load region definitions from a CSV file

import csv

def load_regions_from_csv(filename="regions.csv"):
    regions = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            regions[row["city"]] = {
                "maintenance_multiplier": float(row["maintenance_multiplier"]),
                "strictness": float(row["strictness"])
            }
    return regions

if __name__ == "__main__":
    regions = load_regions_from_csv()
    print("Loaded regions:", regions)
