Licensed Under Creative Commons Attribution Open Source

# 2dayprorate Regional Simulator

This module provides a full regional rent simulation engine including:

- Regional maintenance multipliers  
- Collapsed maintenance (Tama factor)  
- Profit per unit  
- Eviction probability  
- CSV export  
- Modular region definitions  

## Files

### `regions.py`
Contains all region definitions:
- Portland
- Seattle
- Bellingham
- Tacoma
- Eugene
- Los Angeles
- Billings
- Sacramento

Each region includes:
- `maintenance_multiplier`
- `strictness`

### `simulator.py`
Runs the full simulation:
- Imports `regions.py`
- Computes maintenance, profit, and eviction probability
- Prints a formatted table
- Optional CSV export

## Running
# 2dayprorate — Regional Rent & Eviction Simulator

This project provides a modular simulation engine for analyzing:

- Regional maintenance multipliers  
- Collapsed maintenance (Tama factor)  
- Profit per unit  
- Eviction probability  
- Multi-rent batch simulations  
- JSON and CSV region loading  
- Optional HTTP API interface  

The system is fully modular and supports manual region entry, JSON-based region files, CSV-based region files, and automated table generation.

---

## File Overview

### `regional_simulator.py`
Core engine providing:
- Maintenance collapse
- Eviction probability model
- Region simulation
- Interactive region entry

This file contains **no preset regions**.  
Regions can be entered manually or loaded from JSON/CSV.

---

### `json_loader.py`
Loads region definitions from `regions.json`.

Example format:

```json
{
    "Portland, OR": { "maintenance_multiplier": 1.00, "strictness": 0.55 },
    "Seattle, WA": { "maintenance_multiplier": 1.30, "strictness": 0.65 }
}

```bash


python3 simulator.py

To export CSV:

bash
python3 simulator.py
Uncomment the export_csv() line in simulator.py.

Code

---

If you want, I can also generate:

- **`table.py`** for multi‑rent (500–1000) output  
- **`heatmap.py`** for eviction visualization  
- **`api.py`** to expose the simulator as a REST endpoint  

Just tell me the next module you want.
