#!/usr/bin/env python3
# web_api.py
# HTTP API for regional rent simulation

from flask import Flask, request, jsonify
import json
from regional_simulator import simulate_region

app = Flask(__name__)

# Load regions from JSON
with open("data/regions.json", "r") as f:
    REGIONS = json.load(f)

@app.route("/simulate")
def simulate():
    city = request.args.get("city")
    rent = float(request.args.get("rent", 600))

    if city not in REGIONS:
        return jsonify({"error": "City not found"}), 404

    data = REGIONS[city]
    result = simulate_region(
        rent=rent,
        maintenance_multiplier=data["maintenance_multiplier"],
        strictness=data["strictness"]
    )
    return jsonify({"city": city, **result})

@app.route("/batch")
def batch():
    rent = float(request.args.get("rent", 600))
    output = {}

    for city, data in REGIONS.items():
        output[city] = simulate_region(
            rent=rent,
            maintenance_multiplier=data["maintenance_multiplier"],
            strictness=data["strictness"]
        )

    return jsonify(output)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
