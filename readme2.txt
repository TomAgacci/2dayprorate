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
