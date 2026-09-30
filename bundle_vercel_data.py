import os
import json
import itertools
import shutil

DATA_DIR = os.path.abspath("data")
FRONTEND_DATA_DIR = os.path.abspath("frontend/src/data")
FRONTEND_PUBLIC_TILES = os.path.abspath("frontend/public/tiles")

os.makedirs(FRONTEND_DATA_DIR, exist_ok=True)
os.makedirs(FRONTEND_PUBLIC_TILES, exist_ok=True)

# 1. Copy satellite tiles to frontend/public/tiles
tiles_src = os.path.join(DATA_DIR, "tiles")
for f in os.listdir(tiles_src):
    if f.endswith(".png"):
        shutil.copy2(os.path.join(tiles_src, f), os.path.join(FRONTEND_PUBLIC_TILES, f))
print("Copied satellite tiles to frontend/public/tiles")

# 2. Bundle scenario data
with open(os.path.join(DATA_DIR, "fani_track.geojson"), "r", encoding="utf-8") as f:
    fani_track = json.load(f)
with open(os.path.join(DATA_DIR, "infrastructure_assets.geojson"), "r", encoding="utf-8") as f:
    assets = json.load(f)
with open(os.path.join(DATA_DIR, "road_corridors.geojson"), "r", encoding="utf-8") as f:
    roads = json.load(f)
with open(os.path.join(DATA_DIR, "discrete_surge_polygons.geojson"), "r", encoding="utf-8") as f:
    surge_polygons = json.load(f)
with open(os.path.join(DATA_DIR, "infrastructure_edges.json"), "r", encoding="utf-8") as f:
    edges = json.load(f)

from api.main import MITIGATION_CATALOG, cascade_engine, generate_triage_directives, TRACK_BY_OFFSET

scenario_bundle = {
    "scenario_id": "CYCLONE_FANI_2019",
    "name": "Super Cyclone Fani (May 2019) Landfall Simulation",
    "target_region": "Puri - Paradip Coastal Corridor, Odisha, India",
    "track": fani_track,
    "assets": assets,
    "roads": roads,
    "surge_polygons": surge_polygons,
    "edges": edges,
    "mitigation_catalog": MITIGATION_CATALOG
}

with open(os.path.join(FRONTEND_DATA_DIR, "scenario_fani.json"), "w", encoding="utf-8") as f:
    json.dump(scenario_bundle, f)
print("Saved scenario_fani.json")

# 3. Precompute all 208 simulation states
offsets = sorted(TRACK_BY_OFFSET.keys())
mitigation_ids = [m["id"] for m in MITIGATION_CATALOG]

subsets = []
for r in range(len(mitigation_ids) + 1):
    for combo in itertools.combinations(mitigation_ids, r):
        subsets.append(list(combo))

precomputed = {}
for offset in offsets:
    cyclone_step = TRACK_BY_OFFSET[offset]
    for m_combo in subsets:
        combo_key = f"{offset}__" + "__".join(sorted(m_combo))
        cascade_res = cascade_engine.simulate_step(cyclone_step, m_combo)
        triage_res = generate_triage_directives(cascade_res)
        precomputed[combo_key] = {
            "status": "SUCCESS",
            "timeline": {
                "t_offset_hours": offset,
                "timestamp_utc": cyclone_step.get("timestamp_utc", ""),
                "category": cyclone_step.get("category", ""),
                "description": cyclone_step.get("description", "")
            },
            "cyclone_state": {
                "latitude": cyclone_step.get("latitude"),
                "longitude": cyclone_step.get("longitude"),
                "central_pressure_hpa": cyclone_step.get("central_pressure_hpa"),
                "max_sustained_wind_kmph": cyclone_step.get("max_sustained_wind_kmph"),
                "radius_max_winds_km": cyclone_step.get("radius_max_winds_km")
            },
            "summary_metrics": cascade_res["summary_metrics"],
            "nodes": cascade_res["nodes"],
            "roads": cascade_res["roads"],
            "active_mitigations": m_combo,
            "triage": triage_res
        }

with open(os.path.join(FRONTEND_DATA_DIR, "simulation_states.json"), "w", encoding="utf-8") as f:
    json.dump(precomputed, f)
print("Saved simulation_states.json with 208 states")

# 4. Multimodal Tiles
from services.multimodal_vision import AVAILABLE_TILES
tiles_data = [
    {
        "id": k,
        "name": v["name"],
        "coordinates": v["coordinates"],
        "image_url": f"/tiles/{v['file']}"
    }
    for k, v in AVAILABLE_TILES.items()
]
with open(os.path.join(FRONTEND_DATA_DIR, "multimodal_tiles.json"), "w", encoding="utf-8") as f:
    json.dump({
        "tiles": tiles_data,
        "details": AVAILABLE_TILES
    }, f)
print("Saved multimodal_tiles.json")
