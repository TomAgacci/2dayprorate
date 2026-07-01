# json_loader.py
# Load region definitions from a JSON file

import json

def load_regions_from_json(filename="regions.json"):
    with open(filename, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    regions = load_regions_from_json()
    print("Loaded regions:", regions)
