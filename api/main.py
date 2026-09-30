"""
main.py - FastAPI Application for AegisSurge.
Endpoints:
- GET  /health: Health check endpoint.
- GET  /api/scenario/fani: Baseline Cyclone Fani track, infrastructure, roads, surge polygons, and mitigation catalog.
- POST /api/simulate/step: Deterministic physics + NetworkX cascade simulation + Gemini/Heuristic incident triage.
"""

import json
import os
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from aegis_core.cascade_graph import InfrastructureCascadeEngine
from services.vertex_agent import generate_triage_directives
from services.bigquery_service import bigquery_service
from services.multimodal_vision import analyze_satellite_tile, AVAILABLE_TILES, TILES_DIR

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

app = FastAPI(
    title="Aegis API",
    description="Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster",
    version="1.0.0"
)

# Enable CORS for local Next.js frontend and cloud deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize simulation engine
cascade_engine = InfrastructureCascadeEngine(data_dir=DATA_DIR)

# Load pre-cached datasets
with open(os.path.join(DATA_DIR, "fani_track.geojson"), "r", encoding="utf-8") as f:
    FANI_TRACK_GEOJSON = json.load(f)

with open(os.path.join(DATA_DIR, "infrastructure_assets.geojson"), "r", encoding="utf-8") as f:
    ASSETS_GEOJSON = json.load(f)

with open(os.path.join(DATA_DIR, "road_corridors.geojson"), "r", encoding="utf-8") as f:
    ROADS_GEOJSON = json.load(f)

with open(os.path.join(DATA_DIR, "discrete_surge_polygons.geojson"), "r", encoding="utf-8") as f:
    SURGE_GEOJSON = json.load(f)

with open(os.path.join(DATA_DIR, "infrastructure_edges.json"), "r", encoding="utf-8") as f:
    EDGES_DATA = json.load(f)

# Extract track point lookup by t_offset_hours
TRACK_BY_OFFSET = {}
for feat in FANI_TRACK_GEOJSON["features"]:
    if feat["geometry"]["type"] == "Point":
        props = feat["properties"]
        TRACK_BY_OFFSET[props["t_offset_hours"]] = props

MITIGATION_CATALOG = [
    {
        "id": "BERM_SUB_PURI_132",
        "name": "Deploy Rapid Inflatable Flood Berms at Puri 132kV Substation",
        "target": "SUB_PURI_132",
        "description": "Increases transformer yard flood barrier by +1.6m, shielding switchgear from storm surge.",
        "deployment_time_hours": 2.0
    },
    {
        "id": "DEPLOY_DG_HOSP_PURI_DHH",
        "name": "Mobilize 500kVA Auxiliary Mobile Generator to Puri DHH",
        "target": "HOSP_PURI_DHH",
        "description": "Provides +24 hours of autonomous emergency power for ICU and oxygen plant.",
        "deployment_time_hours": 1.5
    },
    {
        "id": "BERM_SUB_PARADIP_132",
        "name": "Erect Demountable Surge Barriers at Paradip 132kV Substation",
        "target": "SUB_PARADIP_132",
        "description": "Protects coastal bulk power transmission feeding Paradip port and water intakes.",
        "deployment_time_hours": 2.5
    },
    {
        "id": "REINFORCE_SUB_GOP_33",
        "name": "Structural Bracing at Gop 33kV Substation",
        "target": "SUB_GOP_33",
        "description": "Increases wind shear resistance threshold to 195 kmph, preventing gantry collapse.",
        "deployment_time_hours": 3.0
    }
]

class SimulateStepRequest(BaseModel):
    t_offset_hours: int = Field(default=0, ge=-12, le=12, description="Hours offset from landfall (-12 to +12)")
    active_mitigations: List[str] = Field(default_factory=list, description="List of mitigation IDs")
    custom_track_point: Optional[Dict[str, Any]] = Field(default=None, description="Optional custom cyclone parameters")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Aegis Simulation Core",
        "version": "1.0.0",
        "total_assets": len(ASSETS_GEOJSON["features"]),
        "track_points_cached": len(TRACK_BY_OFFSET)
    }

@app.get("/api/scenario/fani")
def get_fani_scenario():
    """
    Returns baseline datasets required for initial rendering on the Next.js Deck.gl client.
    """
    return {
        "scenario_id": "CYCLONE_FANI_2019",
        "name": "Super Cyclone Fani (May 2019) Landfall Simulation",
        "target_region": "Puri - Paradip Coastal Corridor, Odisha, India",
        "track": FANI_TRACK_GEOJSON,
        "assets": ASSETS_GEOJSON,
        "roads": ROADS_GEOJSON,
        "surge_polygons": SURGE_GEOJSON,
        "edges": EDGES_DATA,
        "mitigation_catalog": MITIGATION_CATALOG
    }

@app.post("/api/simulate/step")
def simulate_step(payload: SimulateStepRequest):
    """
    Executes a single simulation step:
    1. Retrieves cyclone parameters for the requested timeline step.
    2. Runs Holland wind model and storm-surge bathymetric calculations.
    3. Propagates topological cascades across the power, water, and road networks.
    4. Evaluates cognitive triage directives using Gemini 2.0 Flash (or heuristic fallback).
    """
    # 1. Determine cyclone parameters
    if payload.custom_track_point:
        cyclone_step = payload.custom_track_point
    else:
        cyclone_step = TRACK_BY_OFFSET.get(payload.t_offset_hours)
        if cyclone_step is None:
            # Fall back to nearest known step
            nearest_offset = min(TRACK_BY_OFFSET.keys(), key=lambda k: abs(k - payload.t_offset_hours))
            cyclone_step = TRACK_BY_OFFSET[nearest_offset]

    # 2. Run deterministic physics & NetworkX cascade solver
    cascade_result = cascade_engine.simulate_step(
        cyclone_step=cyclone_step,
        active_mitigations=payload.active_mitigations
    )

    # 3. Cognitive triage reasoning (Gemini Flash or Heuristic Fallback)
    triage_result = generate_triage_directives(cascade_result)

    # 4. Synthesize response
    return {
        "status": "SUCCESS",
        "timeline": {
            "t_offset_hours": payload.t_offset_hours,
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
        "summary_metrics": cascade_result["summary_metrics"],
        "nodes": cascade_result["nodes"],
        "roads": cascade_result["roads"],
        "active_mitigations": payload.active_mitigations,
        "triage": triage_result
    }

@app.get("/api/bigquery/status")
def get_bigquery_status():
    """Returns BigQuery GIS deployment status and spatial index stats."""
    return bigquery_service.get_status()

@app.get("/api/bigquery/cone-assets")
def get_cone_assets(lat: float = 19.80, lon: float = 85.85, buffer_km: float = 50.0):
    """Executes BigQuery GIS ST_DWITHIN cone intersection query."""
    return {
        "query": f"ST_DWITHIN(asset.geom, ST_GeogPoint({lon}, {lat}), {buffer_km} * 1000)",
        "spatial_predicate": "ST_DWITHIN",
        "buffer_km": buffer_km,
        "assets_intersected": bigquery_service.query_cone_assets(lat, lon, buffer_km)
    }

@app.get("/api/bigquery/plinth-analysis")
def get_plinth_analysis(peak_surge_m: float = 3.5):
    """Executes BigQuery GIS hydro-spatial plinth breach ranking."""
    return {
        "spatial_predicate": "ST_DISTANCE + Overland Exponential Decay",
        "peak_surge_m": peak_surge_m,
        "vulnerabilities": bigquery_service.query_plinth_vulnerabilities(peak_surge_m)
    }

@app.get("/api/bigquery/severed-roads")
def get_severed_roads(peak_surge_m: float = 3.5):
    """Executes BigQuery GIS ST_INTERSECTS road severance analysis."""
    return {
        "spatial_predicate": "ST_INTERSECTS(road.path_geom, surge.contour_geom)",
        "peak_surge_m": peak_surge_m,
        "severed_corridors": bigquery_service.query_severed_roads(peak_surge_m)
    }

@app.get("/api/tiles/{filename}")
def get_tile_image(filename: str):
    """Serves high-resolution multi-spectral satellite imagery tiles."""
    file_path = os.path.join(TILES_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Tile not found")

@app.get("/api/multimodal/tiles")
def list_multimodal_tiles():
    """Returns available Sentinel-2 imagery crops for multimodal analysis."""
    return [
        {
            "id": k,
            "name": v["name"],
            "coordinates": v["coordinates"],
            "image_url": f"/api/tiles/{v['file']}"
        }
        for k, v in AVAILABLE_TILES.items()
    ]

class InspectTileRequest(BaseModel):
    tile_id: str

@app.post("/api/multimodal/inspect-tile")
def inspect_tile_endpoint(payload: InspectTileRequest):
    """Executes Gemini 2.0 Flash multimodal vision inference on satellite tile."""
    return analyze_satellite_tile(payload.tile_id)


