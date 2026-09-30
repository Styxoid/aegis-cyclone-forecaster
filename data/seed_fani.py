"""
seed_fani.py - Generates baseline datasets for AegisSurge Track 05:
1. Cyclone Fani (May 2019) high-resolution trajectory (T-12h to T+12h).
2. Critical infrastructure nodes (substations, hospitals, water pumps, shelters, fuel depots) in Puri/Paradip/Khordha.
3. Road corridor network (NH-316, SH-13, NH-53, local arterial links).
4. Infrastructure dependency edges (power, water, access).
5. Discrete coastal storm-surge contour polygons for coastal Odisha.
"""

import json
import os
from typing import Dict, Any, List

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_fani_track() -> Dict[str, Any]:
    """
    Historical trajectory of Super Cyclone Fani (May 2-4, 2019).
    Landfall occurred near Puri (~19.80°N, 85.85°E) at ~03:00 UTC on May 3, 2019 (T=0).
    """
    track_points = [
        {
            "step_id": 0,
            "t_offset_hours": -12,
            "timestamp_utc": "2019-05-02T15:00:00Z",
            "latitude": 18.05,
            "longitude": 84.95,
            "central_pressure_hpa": 932.0,
            "max_sustained_wind_kmph": 215.0,
            "radius_max_winds_km": 28.0,
            "forward_speed_kmph": 17.5,
            "bearing_degrees": 38.0,
            "category": "Extremely Severe Cyclonic Storm (Cat 4-5)",
            "description": "Approaching southwest of Puri over open Bay of Bengal"
        },
        {
            "step_id": 1,
            "t_offset_hours": -10,
            "timestamp_utc": "2019-05-02T17:00:00Z",
            "latitude": 18.32,
            "longitude": 85.12,
            "central_pressure_hpa": 932.0,
            "max_sustained_wind_kmph": 215.0,
            "radius_max_winds_km": 28.0,
            "forward_speed_kmph": 18.0,
            "bearing_degrees": 37.0,
            "category": "Extremely Severe Cyclonic Storm",
            "description": "Outer rainbands begin interacting with southern Odisha coast"
        },
        {
            "step_id": 2,
            "t_offset_hours": -8,
            "timestamp_utc": "2019-05-02T19:00:00Z",
            "latitude": 18.62,
            "longitude": 85.30,
            "central_pressure_hpa": 935.0,
            "max_sustained_wind_kmph": 210.0,
            "radius_max_winds_km": 29.0,
            "forward_speed_kmph": 18.2,
            "bearing_degrees": 36.0,
            "category": "Extremely Severe Cyclonic Storm",
            "description": "Storm surge setup begins in Chilika Lake and Devi estuary"
        },
        {
            "step_id": 3,
            "t_offset_hours": -6,
            "timestamp_utc": "2019-05-02T21:00:00Z",
            "latitude": 18.95,
            "longitude": 85.48,
            "central_pressure_hpa": 937.0,
            "max_sustained_wind_kmph": 205.0,
            "radius_max_winds_km": 30.0,
            "forward_speed_kmph": 19.0,
            "bearing_degrees": 35.0,
            "category": "Extremely Severe Cyclonic Storm",
            "description": "Tropical storm-force winds (65+ kmph) reach Puri shoreline"
        },
        {
            "step_id": 4,
            "t_offset_hours": -4,
            "timestamp_utc": "2019-05-02T23:00:00Z",
            "latitude": 19.28,
            "longitude": 85.65,
            "central_pressure_hpa": 940.0,
            "max_sustained_wind_kmph": 200.0,
            "radius_max_winds_km": 30.0,
            "forward_speed_kmph": 19.5,
            "bearing_degrees": 34.0,
            "category": "Extremely Severe Cyclonic Storm",
            "description": "Hurricane-force winds reach Puri; surge reaches +1.5m MSL"
        },
        {
            "step_id": 5,
            "t_offset_hours": -2,
            "timestamp_utc": "2019-05-03T01:00:00Z",
            "latitude": 19.55,
            "longitude": 85.76,
            "central_pressure_hpa": 945.0,
            "max_sustained_wind_kmph": 195.0,
            "radius_max_winds_km": 32.0,
            "forward_speed_kmph": 20.0,
            "bearing_degrees": 32.0,
            "category": "Extremely Severe Cyclonic Storm",
            "description": "Eyewall approaches Puri beach; coastal 33kV substations begin tripping"
        },
        {
            "step_id": 6,
            "t_offset_hours": 0,
            "timestamp_utc": "2019-05-03T03:00:00Z",
            "latitude": 19.80,
            "longitude": 85.85,
            "central_pressure_hpa": 950.0,
            "max_sustained_wind_kmph": 185.0,
            "radius_max_winds_km": 32.0,
            "forward_speed_kmph": 20.5,
            "bearing_degrees": 30.0,
            "category": "Extremely Severe Cyclonic Storm (Landfall)",
            "description": "LANDFALL at Puri. Peak surge of +3.5m MSL. Complete grid disruption."
        },
        {
            "step_id": 7,
            "t_offset_hours": 2,
            "timestamp_utc": "2019-05-03T05:00:00Z",
            "latitude": 20.05,
            "longitude": 86.02,
            "central_pressure_hpa": 962.0,
            "max_sustained_wind_kmph": 155.0,
            "radius_max_winds_km": 35.0,
            "forward_speed_kmph": 21.0,
            "bearing_degrees": 28.0,
            "category": "Very Severe Cyclonic Storm",
            "description": "Inland decay over Khordha/Bhubaneswar; high surge pushing up Mahanadi"
        },
        {
            "step_id": 8,
            "t_offset_hours": 4,
            "timestamp_utc": "2019-05-03T07:00:00Z",
            "latitude": 20.28,
            "longitude": 86.25,
            "central_pressure_hpa": 974.0,
            "max_sustained_wind_kmph": 135.0,
            "radius_max_winds_km": 38.0,
            "forward_speed_kmph": 22.0,
            "bearing_degrees": 26.0,
            "category": "Severe Cyclonic Storm",
            "description": "Eye moving towards Jagatsinghpur; Paradip port reports 130 kmph gusts"
        },
        {
            "step_id": 9,
            "t_offset_hours": 6,
            "timestamp_utc": "2019-05-03T09:00:00Z",
            "latitude": 20.52,
            "longitude": 86.52,
            "central_pressure_hpa": 984.0,
            "max_sustained_wind_kmph": 115.0,
            "radius_max_winds_km": 42.0,
            "forward_speed_kmph": 23.0,
            "bearing_degrees": 25.0,
            "category": "Cyclonic Storm",
            "description": "Passing over Paradip & Kendrapada; storm surge receding at Puri"
        },
        {
            "step_id": 10,
            "t_offset_hours": 8,
            "timestamp_utc": "2019-05-03T11:00:00Z",
            "latitude": 20.80,
            "longitude": 86.82,
            "central_pressure_hpa": 992.0,
            "max_sustained_wind_kmph": 95.0,
            "radius_max_winds_km": 45.0,
            "forward_speed_kmph": 24.0,
            "bearing_degrees": 25.0,
            "category": "Cyclonic Storm",
            "description": "Heading into Bhadrak and Balasore corridor"
        },
        {
            "step_id": 11,
            "t_offset_hours": 10,
            "timestamp_utc": "2019-05-03T13:00:00Z",
            "latitude": 21.10,
            "longitude": 87.15,
            "central_pressure_hpa": 998.0,
            "max_sustained_wind_kmph": 80.0,
            "radius_max_winds_km": 48.0,
            "forward_speed_kmph": 25.0,
            "bearing_degrees": 26.0,
            "category": "Deep Depression",
            "description": "Passing into West Bengal boundary"
        },
        {
            "step_id": 12,
            "t_offset_hours": 12,
            "timestamp_utc": "2019-05-03T15:00:00Z",
            "latitude": 21.45,
            "longitude": 87.55,
            "central_pressure_hpa": 1004.0,
            "max_sustained_wind_kmph": 65.0,
            "radius_max_winds_km": 50.0,
            "forward_speed_kmph": 26.0,
            "bearing_degrees": 28.0,
            "category": "Depression",
            "description": "System weakened over Gangetic West Bengal"
        }
    ]

    features = []
    # LineString of entire track
    line_coords = [[p["longitude"], p["latitude"]] for p in track_points]
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": line_coords
        },
        "properties": {
            "name": "Cyclone Fani Trajectory Line",
            "total_steps": len(track_points)
        }
    })

    # Individual Point features
    for p in track_points:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p["longitude"], p["latitude"]]
            },
            "properties": p
        })

    return {
        "type": "FeatureCollection",
        "name": "CycloneFaniTrack",
        "metadata": {
            "storm_name": "FANI",
            "year": 2019,
            "ocean_basin": "North Indian Ocean",
            "landfall_point": [85.85, 19.80]
        },
        "features": features
    }

def generate_infrastructure_assets() -> Dict[str, Any]:
    """
    Critical infrastructure nodes across Puri, Khordha, and Jagatsinghpur/Paradip.
    Nodes include:
    - Electrical substations (132kV, 33kV)
    - Hospitals & CHCs
    - Water treatment / lift pumping stations
    - Multipurpose Cyclone Shelters (MCS)
    - Fuel storage depots
    """
    nodes = [
        # --- Electrical Substations ---
        {
            "id": "SUB_PURI_132",
            "name": "Puri 132/33kV Main Grid Substation",
            "type": "SUBSTATION",
            "district": "Puri",
            "lat": 19.8250,
            "lon": 85.8320,
            "plinth_height_m": 1.2,
            "wind_threshold_kmph": 175.0,
            "capacity_mva": 160,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Primary high-voltage bulk transmission substation for Puri urban and pilgrim core."
        },
        {
            "id": "SUB_GOP_33",
            "name": "Gop 33/11kV Distribution Substation",
            "type": "SUBSTATION",
            "district": "Puri",
            "lat": 19.9980,
            "lon": 86.0120,
            "plinth_height_m": 0.8,
            "wind_threshold_kmph": 160.0,
            "capacity_mva": 25,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Feeds rural agricultural pumping and Gop Community Health Centre."
        },
        {
            "id": "SUB_NIMAPADA_33",
            "name": "Nimapada 33/11kV Substation",
            "type": "SUBSTATION",
            "district": "Puri",
            "lat": 20.0650,
            "lon": 85.9850,
            "plinth_height_m": 1.5,
            "wind_threshold_kmph": 170.0,
            "capacity_mva": 30,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Inland sub-transmission hub feeding Nimapada town and storage depots."
        },
        {
            "id": "SUB_PARADIP_132",
            "name": "Paradip Port 132/33kV Substation",
            "type": "SUBSTATION",
            "district": "Jagatsinghpur",
            "lat": 20.2950,
            "lon": 86.6720,
            "plinth_height_m": 1.1,
            "wind_threshold_kmph": 175.0,
            "capacity_mva": 120,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Powers Paradip Port logistics, IOCL oil refinery inputs, and regional coastal grid."
        },
        {
            "id": "SUB_KUJANG_33",
            "name": "Kujang 33/11kV Substation",
            "type": "SUBSTATION",
            "district": "Jagatsinghpur",
            "lat": 20.3150,
            "lon": 86.5350,
            "plinth_height_m": 1.0,
            "wind_threshold_kmph": 165.0,
            "capacity_mva": 20,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Feeds Kujang coastal belt, lift irrigation, and emergency shelters."
        },
        {
            "id": "SUB_ASTARANGA_33",
            "name": "Astaranga 33/11kV Coastal Substation",
            "type": "SUBSTATION",
            "district": "Puri",
            "lat": 19.9820,
            "lon": 86.2650,
            "plinth_height_m": 0.6,
            "wind_threshold_kmph": 155.0,
            "capacity_mva": 15,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Vulnerable low-lying fishing harbour substation near Devi river mouth."
        },

        # --- Hospitals & Healthcare ---
        {
            "id": "HOSP_PURI_DHH",
            "name": "Puri District Headquarters Hospital (DHH)",
            "type": "HOSPITAL",
            "district": "Puri",
            "lat": 19.8140,
            "lon": 85.8240,
            "plinth_height_m": 1.8,
            "wind_threshold_kmph": 210.0,
            "bed_capacity": 450,
            "backup_generator_hours": 12.0,
            "criticality": "P0_LIFE_CRITICAL",
            "description": "Apex tertiary trauma, ICU, and surgical facility for Puri district."
        },
        {
            "id": "HOSP_GOP_CHC",
            "name": "Gop Community Health Centre",
            "type": "HOSPITAL",
            "district": "Puri",
            "lat": 20.0020,
            "lon": 86.0090,
            "plinth_height_m": 1.4,
            "wind_threshold_kmph": 190.0,
            "bed_capacity": 60,
            "backup_generator_hours": 6.0,
            "criticality": "P0_LIFE_CRITICAL",
            "description": "Primary maternity and emergency stabilization center for Gop rural block."
        },
        {
            "id": "HOSP_NIMAPADA_SDH",
            "name": "Nimapada Sub-Divisional Hospital",
            "type": "HOSPITAL",
            "district": "Puri",
            "lat": 20.0710,
            "lon": 85.9810,
            "plinth_height_m": 2.2,
            "wind_threshold_kmph": 220.0,
            "bed_capacity": 100,
            "backup_generator_hours": 14.0,
            "criticality": "P0_LIFE_CRITICAL",
            "description": "Inland backup hospital equipped with solar-diesel hybrid backup power."
        },
        {
            "id": "HOSP_PARADIP_PORT",
            "name": "Paradip Port Trust Hospital",
            "type": "HOSPITAL",
            "district": "Jagatsinghpur",
            "lat": 20.2880,
            "lon": 86.6650,
            "plinth_height_m": 1.6,
            "wind_threshold_kmph": 205.0,
            "bed_capacity": 120,
            "backup_generator_hours": 10.0,
            "criticality": "P0_LIFE_CRITICAL",
            "description": "Industrial and maritime medical center serving 15,000 dock and port workers."
        },
        {
            "id": "HOSP_KUJANG_CHC",
            "name": "Kujang Community Health Centre",
            "type": "HOSPITAL",
            "district": "Jagatsinghpur",
            "lat": 20.3180,
            "lon": 86.5310,
            "plinth_height_m": 1.3,
            "wind_threshold_kmph": 185.0,
            "bed_capacity": 50,
            "backup_generator_hours": 8.0,
            "criticality": "P0_LIFE_CRITICAL",
            "description": "Key emergency medical outpost for Ersama and Kujang cyclone belts."
        },

        # --- Water Treatment & Pumping ---
        {
            "id": "WATER_PURI_MAIN",
            "name": "Puri Municipal Water Treatment Plant",
            "type": "WATER_PUMP",
            "district": "Puri",
            "lat": 19.8320,
            "lon": 85.8150,
            "plinth_height_m": 1.0,
            "wind_threshold_kmph": 180.0,
            "capacity_mld": 45,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Treats sweet water aquifer supplies for 200,000 Puri residents and hospitals."
        },
        {
            "id": "WATER_GOP_LIFT",
            "name": "Kushabhadra River Intake & Lift Station",
            "type": "WATER_PUMP",
            "district": "Puri",
            "lat": 20.0150,
            "lon": 86.0250,
            "plinth_height_m": 0.7,
            "wind_threshold_kmph": 170.0,
            "capacity_mld": 15,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Pumps potable canal water to Gop and surrounding 40 gram panchayats."
        },
        {
            "id": "WATER_PARADIP_INTAKE",
            "name": "Taladanda Canal Water Intake & Treatment",
            "type": "WATER_PUMP",
            "district": "Jagatsinghpur",
            "lat": 20.3010,
            "lon": 86.6200,
            "plinth_height_m": 1.2,
            "wind_threshold_kmph": 185.0,
            "capacity_mld": 60,
            "criticality": "P1_INFRA_BACKBONE",
            "description": "Primary drinking and industrial raw water intake for Paradip municipal area."
        },

        # --- Cyclone Shelters (MCS) ---
        {
            "id": "SHELTER_CHANDRABHAGA",
            "name": "Chandrabhaga Multipurpose Cyclone Shelter",
            "type": "SHELTER",
            "district": "Puri",
            "lat": 19.8720,
            "lon": 86.1150,
            "plinth_height_m": 3.5,
            "wind_threshold_kmph": 240.0,
            "capacity_persons": 2500,
            "criticality": "P3_CIVIC_SHELTER",
            "description": "Engineered two-storey reinforced concrete cyclone refuge with stilt ground floor."
        },
        {
            "id": "SHELTER_ASTARANGA",
            "name": "Astaranga Coastal Refuge Shelter",
            "type": "SHELTER",
            "district": "Puri",
            "lat": 19.9750,
            "lon": 86.2580,
            "plinth_height_m": 3.0,
            "wind_threshold_kmph": 230.0,
            "capacity_persons": 1800,
            "criticality": "P3_CIVIC_SHELTER",
            "description": "High-capacity concrete shelter equipped with hand-cranked satellite radios."
        },
        {
            "id": "SHELTER_PURI_BALIAPANDA",
            "name": "Baliapanda Cyclone Shelter",
            "type": "SHELTER",
            "district": "Puri",
            "lat": 19.7890,
            "lon": 85.8050,
            "plinth_height_m": 2.8,
            "wind_threshold_kmph": 230.0,
            "capacity_persons": 3000,
            "criticality": "P3_CIVIC_SHELTER",
            "description": "Designated for coastal fishing hamlets along Puri's vulnerable southern spit."
        },
        {
            "id": "SHELTER_ERSAMA_MCS",
            "name": "Ersama Block Multipurpose Shelter",
            "type": "SHELTER",
            "district": "Jagatsinghpur",
            "lat": 20.1980,
            "lon": 86.4850,
            "plinth_height_m": 3.8,
            "wind_threshold_kmph": 250.0,
            "capacity_persons": 3500,
            "criticality": "P3_CIVIC_SHELTER",
            "description": "Historical high-plinth fortress shelter constructed following the 1999 Super Cyclone."
        },
        {
            "id": "SHELTER_PARADIP_LOCK",
            "name": "Paradip Lock Gate Cyclone Shelter",
            "type": "SHELTER",
            "district": "Jagatsinghpur",
            "lat": 20.2780,
            "lon": 86.6450,
            "plinth_height_m": 3.2,
            "wind_threshold_kmph": 240.0,
            "capacity_persons": 2200,
            "criticality": "P3_CIVIC_SHELTER",
            "description": "Emergency refuge for informal slum settlements near port canal lock gates."
        },

        # --- Fuel Depots & Strategic Logistics ---
        {
            "id": "FUEL_PURI_DEPOT",
            "name": "Puri IOCL Emergency Fuel Reserves",
            "type": "FUEL_DEPOT",
            "district": "Puri",
            "lat": 19.8350,
            "lon": 85.8450,
            "plinth_height_m": 1.5,
            "wind_threshold_kmph": 200.0,
            "capacity_kl": 500,
            "criticality": "P2_LOGISTICS",
            "description": "Main diesel supply yard for district emergency generators and hospital tankers."
        },
        {
            "id": "FUEL_PARADIP_TERMINAL",
            "name": "Paradip Strategic Fuel Bulk Terminal",
            "type": "FUEL_DEPOT",
            "district": "Jagatsinghpur",
            "lat": 20.2850,
            "lon": 86.6800,
            "plinth_height_m": 2.5,
            "wind_threshold_kmph": 220.0,
            "capacity_kl": 5000,
            "criticality": "P2_LOGISTICS",
            "description": "Massive coastal petroleum storage supporting maritime, rail, and road tankers."
        }
    ]

    features = []
    for node in nodes:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [node["lon"], node["lat"]]
            },
            "properties": node
        })

    return {
        "type": "FeatureCollection",
        "name": "InfrastructureAssets",
        "features": features
    }

def generate_road_corridors() -> Dict[str, Any]:
    """
    Arterial logistics corridors connecting substations, hospitals, and shelters:
    - NH-316: Bhubaneswar - Pipili - Puri Arterial Expressway
    - SH-13: Konark - Puri Marine Drive Scenic Highway (High coastal surge exposure)
    - Gop - Nimapada Link Road (Critical inland bypass)
    - NH-53: Cuttack - Kujang - Paradip Port Corridor
    - Ersama - Paradip Coastal Feeder Road
    """
    roads = [
        {
            "id": "ROAD_NH316_PURI",
            "name": "NH-316 Puri Arterial Corridor",
            "type": "HIGHWAY",
            "elevation_m": 2.1,
            "max_wading_depth_m": 0.35,
            "coordinates": [
                [85.8320, 19.8250],
                [85.8240, 19.8140],
                [85.8400, 19.8800],
                [85.8600, 19.9500],
                [85.8500, 20.0200]
            ],
            "connects": ["HOSP_PURI_DHH", "SUB_PURI_132", "FUEL_PURI_DEPOT"]
        },
        {
            "id": "ROAD_SH13_MARINEDRIVE",
            "name": "SH-13 Puri-Konark Marine Drive",
            "type": "COASTAL_HIGHWAY",
            "elevation_m": 0.9,  # High surge vulnerability!
            "max_wading_depth_m": 0.30,
            "coordinates": [
                [85.8320, 19.8250],
                [85.9500, 19.8400],
                [86.0500, 19.8600],
                [86.1150, 19.8720]
            ],
            "connects": ["SUB_PURI_132", "SHELTER_CHANDRABHAGA"]
        },
        {
            "id": "ROAD_GOP_NIMAPADA_LINK",
            "name": "Gop-Nimapada Inland Bypass",
            "type": "SECONDARY_ROAD",
            "elevation_m": 3.2,  # Safe high ground!
            "max_wading_depth_m": 0.40,
            "coordinates": [
                [86.0120, 19.9980],
                [86.0090, 20.0020],
                [85.9950, 20.0350],
                [85.9850, 20.0650],
                [85.9810, 20.0710]
            ],
            "connects": ["SUB_GOP_33", "HOSP_GOP_CHC", "SUB_NIMAPADA_33", "HOSP_NIMAPADA_SDH"]
        },
        {
            "id": "ROAD_NH53_PARADIP",
            "name": "NH-53 Cuttack-Paradip Port Expressway",
            "type": "EXPRESSWAY",
            "elevation_m": 2.4,
            "max_wading_depth_m": 0.35,
            "coordinates": [
                [86.5350, 20.3150],
                [86.5310, 20.3180],
                [86.6200, 20.3010],
                [86.6650, 20.2880],
                [86.6720, 20.2950]
            ],
            "connects": ["SUB_KUJANG_33", "HOSP_KUJANG_CHC", "WATER_PARADIP_INTAKE", "HOSP_PARADIP_PORT", "SUB_PARADIP_132"]
        },
        {
            "id": "ROAD_ERSAMA_PARADIP",
            "name": "Ersama-Paradip Coastal Link",
            "type": "RURAL_CORRIDOR",
            "elevation_m": 1.1,
            "max_wading_depth_m": 0.25,
            "coordinates": [
                [86.4850, 20.1980],
                [86.5600, 20.2400],
                [86.6450, 20.2780]
            ],
            "connects": ["SHELTER_ERSAMA_MCS", "SHELTER_PARADIP_LOCK"]
        }
    ]

    features = []
    for r in roads:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": r["coordinates"]
            },
            "properties": r
        })

    return {
        "type": "FeatureCollection",
        "name": "RoadCorridors",
        "features": features
    }

def generate_infrastructure_edges() -> List[Dict[str, Any]]:
    """
    Physical and functional dependency edges connecting nodes in the system.
    Edges are directed: source -> target.
    e.g., source SUB_PURI_132 powers target HOSP_PURI_DHH.
    """
    return [
        # --- Power Grid Dependencies (Substations -> Facilities) ---
        {"source": "SUB_PURI_132", "target": "HOSP_PURI_DHH", "type": "POWER", "description": "11kV feeder line powering Puri DHH"},
        {"source": "SUB_PURI_132", "target": "WATER_PURI_MAIN", "type": "POWER", "description": "Dedicated line to Puri Water Works"},
        {"source": "SUB_PURI_132", "target": "FUEL_PURI_DEPOT", "type": "POWER", "description": "Feeder to IOCL fuel terminal"},
        {"source": "SUB_PURI_132", "target": "SHELTER_PURI_BALIAPANDA", "type": "POWER", "description": "Power to Baliapanda cyclone shelter"},
        {"source": "SUB_GOP_33", "target": "HOSP_GOP_CHC", "type": "POWER", "description": "Feeder to Gop Community Health Centre"},
        {"source": "SUB_GOP_33", "target": "WATER_GOP_LIFT", "type": "POWER", "description": "Power to Kushabhadra river lift pump"},
        {"source": "SUB_NIMAPADA_33", "target": "HOSP_NIMAPADA_SDH", "type": "POWER", "description": "Feeder to Nimapada Sub-Divisional Hospital"},
        {"source": "SUB_ASTARANGA_33", "target": "SHELTER_ASTARANGA", "type": "POWER", "description": "Coastal feeder line to Astaranga refuge shelter"},
        {"source": "SUB_PARADIP_132", "target": "HOSP_PARADIP_PORT", "type": "POWER", "description": "Grid power to Paradip Port Trust Hospital"},
        {"source": "SUB_PARADIP_132", "target": "WATER_PARADIP_INTAKE", "type": "POWER", "description": "Main power to Taladanda canal intake"},
        {"source": "SUB_PARADIP_132", "target": "FUEL_PARADIP_TERMINAL", "type": "POWER", "description": "Power to Paradip bulk fuel pumps"},
        {"source": "SUB_KUJANG_33", "target": "HOSP_KUJANG_CHC", "type": "POWER", "description": "Power to Kujang Community Health Centre"},
        {"source": "SUB_KUJANG_33", "target": "SHELTER_ERSAMA_MCS", "type": "POWER", "description": "Transmission to Ersama multipurpose shelter"},

        # --- Potable Water Dependencies (Pumps -> Facilities) ---
        {"source": "WATER_PURI_MAIN", "target": "HOSP_PURI_DHH", "type": "WATER", "description": "Piped drinking and medical sterilization water supply"},
        {"source": "WATER_GOP_LIFT", "target": "HOSP_GOP_CHC", "type": "WATER", "description": "Drinking water connection to Gop CHC"},
        {"source": "WATER_PARADIP_INTAKE", "target": "HOSP_PARADIP_PORT", "type": "WATER", "description": "Potable and cooling water supply to Port Hospital"},

        # --- Logistics / Fuel Dependencies (Fuel Depots -> Facilities) ---
        {"source": "FUEL_PURI_DEPOT", "target": "HOSP_PURI_DHH", "type": "ACCESS", "description": "Road supply corridor for emergency diesel refueling"},
        {"source": "FUEL_PARADIP_TERMINAL", "target": "HOSP_PARADIP_PORT", "type": "ACCESS", "description": "Direct port access fuel replenishment"},
        {"source": "HOSP_GOP_CHC", "target": "HOSP_NIMAPADA_SDH", "type": "ACCESS", "description": "Patient transfer corridor via Gop-Nimapada link road"}
    ]

def generate_discrete_surge_polygons() -> Dict[str, Any]:
    """
    Pre-computed discrete surge depth contour polygons for the Puri/Paradip coastline.
    Covers the vulnerable coastlines at Chilika spit, Puri beach, Devi river mouth, and Mahanadi estuary.
    Each polygon represents an inundation envelope for different surge severities.
    """
    polygons = [
        # --- Level 1 Surge (0.5m - 1.0m MSL: Low-lying coastal spits & tidal inlets) ---
        {
            "id": "SURGE_CONTOUR_05M",
            "surge_level_m": 0.75,
            "severity": "LOW",
            "name": "0.75m Surge Inundation Envelope (Tidal Flats & Spits)",
            "color": "#00bcd4",
            "coordinates": [
                [
                    [85.7500, 19.7600],
                    [85.8300, 19.7900],
                    [85.9500, 19.8200],
                    [86.1000, 19.8500],
                    [86.2500, 19.9200],
                    [86.3500, 20.0500],
                    [86.5500, 20.2000],
                    [86.7200, 20.3000],
                    [86.7500, 20.2800],
                    [86.5800, 20.1500],
                    [86.3800, 19.9800],
                    [86.1200, 19.8300],
                    [85.9600, 19.8000],
                    [85.8200, 19.7700],
                    [85.7500, 19.7600]
                ]
            ]
        },
        # --- Level 2 Surge (1.5m - 2.0m MSL: Encroaching 1-2 km inland, Devi & Mahanadi rivers) ---
        {
            "id": "SURGE_CONTOUR_15M",
            "surge_level_m": 1.75,
            "severity": "MEDIUM",
            "name": "1.75m Surge Inundation Envelope (Marine Drive & Estuaries)",
            "color": "#0288d1",
            "coordinates": [
                [
                    [85.7400, 19.7550],
                    [85.8100, 19.8000],
                    [85.9200, 19.8350],
                    [86.0800, 19.8700],
                    [86.2200, 19.9600],
                    [86.3000, 20.1200],
                    [86.5200, 20.2400],
                    [86.6900, 20.3200],
                    [86.7300, 20.2700],
                    [86.5000, 20.1200],
                    [86.3200, 19.9400],
                    [86.0900, 19.8400],
                    [85.9100, 19.8100],
                    [85.8000, 19.7800],
                    [85.7400, 19.7550]
                ]
            ]
        },
        # --- Level 3 Surge (2.5m - 3.5m MSL: Catastrophic Landfall Envelope at Puri & Paradip) ---
        {
            "id": "SURGE_CONTOUR_35M",
            "surge_level_m": 3.50,
            "severity": "CRITICAL",
            "name": "3.50m Peak Surge Landfall Inundation Envelope (Puri Core & Ersama Basin)",
            "color": "#d32f2f",
            "coordinates": [
                [
                    [85.7300, 19.7500],
                    [85.8000, 19.8150],
                    [85.8500, 19.8350],
                    [85.9500, 19.8600],
                    [86.1000, 19.9100],
                    [86.2400, 20.0200],
                    [86.4000, 20.1800],
                    [86.6200, 20.3100],
                    [86.7100, 20.3400],
                    [86.7400, 20.2500],
                    [86.5200, 20.1000],
                    [86.3500, 19.9000],
                    [86.1200, 19.8200],
                    [85.9300, 19.7900],
                    [85.7900, 19.7600],
                    [85.7300, 19.7500]
                ]
            ]
        }
    ]

    features = []
    for poly in polygons:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": poly["coordinates"]
            },
            "properties": {
                "id": poly["id"],
                "surge_level_m": poly["surge_level_m"],
                "severity": poly["severity"],
                "name": poly["name"],
                "color": poly["color"]
            }
        })

    return {
        "type": "FeatureCollection",
        "name": "DiscreteSurgePolygons",
        "features": features
    }

def seed_all():
    print(f"[Seed] Generating datasets in {DATA_DIR}...")
    
    track_data = generate_fani_track()
    track_path = os.path.join(DATA_DIR, "fani_track.geojson")
    with open(track_path, "w", encoding="utf-8") as f:
        json.dump(track_data, f, indent=2)
    print(f" -> Wrote {track_path} ({len(track_data['features'])} features)")

    assets_data = generate_infrastructure_assets()
    assets_path = os.path.join(DATA_DIR, "infrastructure_assets.geojson")
    with open(assets_path, "w", encoding="utf-8") as f:
        json.dump(assets_data, f, indent=2)
    print(f" -> Wrote {assets_path} ({len(assets_data['features'])} assets)")

    roads_data = generate_road_corridors()
    roads_path = os.path.join(DATA_DIR, "road_corridors.geojson")
    with open(roads_path, "w", encoding="utf-8") as f:
        json.dump(roads_data, f, indent=2)
    print(f" -> Wrote {roads_path} ({len(roads_data['features'])} corridors)")

    edges_data = generate_infrastructure_edges()
    edges_path = os.path.join(DATA_DIR, "infrastructure_edges.json")
    with open(edges_path, "w", encoding="utf-8") as f:
        json.dump(edges_data, f, indent=2)
    print(f" -> Wrote {edges_path} ({len(edges_data)} edges)")

    surge_data = generate_discrete_surge_polygons()
    surge_path = os.path.join(DATA_DIR, "discrete_surge_polygons.geojson")
    with open(surge_path, "w", encoding="utf-8") as f:
        json.dump(surge_data, f, indent=2)
    print(f" -> Wrote {surge_path} ({len(surge_data['features'])} surge envelopes)")

    print("[Seed] All baseline datasets successfully created!")

if __name__ == "__main__":
    seed_all()
