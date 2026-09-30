"""
cascade_graph.py - NetworkX-based topological infrastructure dependency graph and cascade solver.
Models directed dependencies across:
- 132/33kV Electrical Substations
- Hospitals and Regional Healthcare Facilities
- Water Treatment & Booster Pumping Stations
- Multipurpose Cyclone Shelters (MCS)
- Fuel Depots and Logistics Arterials
- Road Corridors and Bridge Vulnerability
"""

import json
import os
import networkx as nx
from typing import Dict, Any, List, Optional
from aegis_core.physics import (
    haversine_distance_km,
    calculate_azimuth_deg,
    holland_wind_speed_kmph,
    calculate_storm_surge_elevation_m,
    calculate_asset_inundation
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

class InfrastructureCascadeEngine:
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        self.nodes_data: Dict[str, Dict[str, Any]] = {}
        self.edges_data: List[Dict[str, Any]] = []
        self.roads_data: List[Dict[str, Any]] = []
        self.graph = nx.DiGraph()
        self.load_data()

    def load_data(self):
        """Loads infrastructure assets, edges, and road corridors into memory."""
        assets_file = os.path.join(self.data_dir, "infrastructure_assets.geojson")
        with open(assets_file, "r", encoding="utf-8") as f:
            assets_geojson = json.load(f)
            for feat in assets_geojson["features"]:
                props = feat["properties"]
                node_id = props["id"]
                self.nodes_data[node_id] = props

        edges_file = os.path.join(self.data_dir, "infrastructure_edges.json")
        with open(edges_file, "r", encoding="utf-8") as f:
            self.edges_data = json.load(f)

        roads_file = os.path.join(self.data_dir, "road_corridors.geojson")
        with open(roads_file, "r", encoding="utf-8") as f:
            roads_geojson = json.load(f)
            self.roads_data = [feat["properties"] for feat in roads_geojson["features"]]

        self._build_graph()

    def _build_graph(self):
        """Constructs the NetworkX directed multi-dependency graph."""
        self.graph.clear()
        for node_id, props in self.nodes_data.items():
            self.graph.add_node(
                node_id,
                **props,
                state="OPERATIONAL",
                failure_cause="NONE",
                wind_speed_kmph=0.0,
                surge_depth_m=0.0
            )

        for edge in self.edges_data:
            self.graph.add_edge(
                edge["source"],
                edge["target"],
                type=edge["type"],
                description=edge["description"],
                status="ACTIVE"
            )

    def _estimate_dist_to_coast_km(self, lat: float, lon: float) -> float:
        """
        Estimates shortest distance from asset coordinate to the Odisha shoreline.
        Odisha coastline runs approximately along line from (19.75, 85.80) to (20.30, 86.70).
        """
        # Linear approximation to coastline segment
        coast_lat = 19.75 + (lon - 85.80) * (20.30 - 19.75) / (86.70 - 85.80)
        dist_km = haversine_distance_km(lat, lon, coast_lat, lon)
        # If asset is south/east of the shoreline, it's virtually on or in the water
        if lat < coast_lat:
            return 0.1
        return max(0.2, dist_km)

    def simulate_step(
        self,
        cyclone_step: Dict[str, Any],
        active_mitigations: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Simulates physical impacts and cascading topological propagation for a given cyclone time step.
        
        Args:
            cyclone_step: Dictionary containing eye coordinates, wind, pressure, and forward speed.
            active_mitigations: List of action strings, e.g. ["BERM_SUB_PURI_132", "DEPLOY_DG_HOSP_PURI_DHH"]
        """
        if active_mitigations is None:
            active_mitigations = []

        eye_lat = cyclone_step["latitude"]
        eye_lon = cyclone_step["longitude"]
        p_central = cyclone_step["central_pressure_hpa"]
        max_wind = cyclone_step["max_sustained_wind_kmph"]
        r_max = cyclone_step.get("radius_max_winds_km", 30.0)
        forward_speed = cyclone_step.get("forward_speed_kmph", 20.0)
        storm_bearing = cyclone_step.get("bearing_degrees", 35.0)
        t_offset = cyclone_step.get("t_offset_hours", 0)

        # 1. Reset dynamic graph states
        self._build_graph()

        node_states: Dict[str, Dict[str, Any]] = {}

        # 2. Direct Physical Hazard Assessment
        for node_id, data in self.nodes_data.items():
            node_lat = data["lat"]
            node_lon = data["lon"]
            plinth_h = data.get("plinth_height_m", 1.0)
            wind_thresh = data.get("wind_threshold_kmph", 180.0)

            # Check if mitigation raises plinth (e.g. temporary inflatable flood berm)
            if f"BERM_{node_id}" in active_mitigations:
                plinth_h += 1.6  # Flood berm adds 1.6m height protection

            # Check if mitigation reinforces structures against wind
            if f"REINFORCE_{node_id}" in active_mitigations:
                wind_thresh += 35.0

            # Distance & azimuth to cyclone eye
            dist_to_eye = haversine_distance_km(eye_lat, eye_lon, node_lat, node_lon)
            azimuth_to_node = calculate_azimuth_deg(eye_lat, eye_lon, node_lat, node_lon)

            # Wind speed calculation
            wind_kmph = holland_wind_speed_kmph(
                r_km=dist_to_eye,
                p_central_hpa=p_central,
                r_max_km=r_max,
                lat_deg=node_lat,
                forward_speed_kmph=forward_speed,
                storm_bearing_deg=storm_bearing,
                azimuth_to_asset_deg=azimuth_to_node
            )

            # Surge inundation calculation
            dist_to_coast = self._estimate_dist_to_coast_km(node_lat, node_lon)
            surge_water_m = calculate_storm_surge_elevation_m(
                p_central_hpa=p_central,
                max_wind_kmph=max_wind,
                dist_to_coastline_km=dist_to_coast
            )
            surge_depth_m = calculate_asset_inundation(surge_water_m, plinth_h)

            state = "OPERATIONAL"
            failure_cause = "NONE"

            # Check direct physical failure thresholds
            if surge_depth_m > 0.05:
                state = "FAILED"
                failure_cause = "SURGE_INUNDATION"
            elif wind_kmph >= wind_thresh:
                state = "FAILED"
                failure_cause = "DIRECT_WIND"

            node_states[node_id] = {
                "node_id": node_id,
                "name": data["name"],
                "type": data["type"],
                "lat": node_lat,
                "lon": node_lon,
                "district": data.get("district", "Puri"),
                "criticality": data.get("criticality", "P1_INFRA_BACKBONE"),
                "current_wind_speed_kmph": wind_kmph,
                "current_surge_depth_m": surge_depth_m,
                "state": state,
                "failure_cause": failure_cause,
                "backup_hours_remaining": data.get("backup_generator_hours", 0.0),
                "isolated_from_resupply": False,
                "mitigations_active": [m for m in active_mitigations if node_id in m]
            }

            # Update NetworkX node
            self.graph.nodes[node_id]["state"] = state
            self.graph.nodes[node_id]["failure_cause"] = failure_cause
            self.graph.nodes[node_id]["wind_speed_kmph"] = wind_kmph
            self.graph.nodes[node_id]["surge_depth_m"] = surge_depth_m

        # 3. Road Network Vulnerability & Severance Check
        severed_roads = []
        road_statuses = []
        for road in self.roads_data:
            road_id = road["id"]
            # Sample midpoint of road corridor
            coords = road["coordinates"]
            mid_idx = len(coords) // 2
            mid_lon, mid_lat = coords[mid_idx]

            dist_to_coast = self._estimate_dist_to_coast_km(mid_lat, mid_lon)
            surge_water_m = calculate_storm_surge_elevation_m(
                p_central_hpa=p_central,
                max_wind_kmph=max_wind,
                dist_to_coastline_km=dist_to_coast
            )
            inundation_on_road = max(0.0, surge_water_m - road.get("elevation_m", 1.5))
            is_severed = inundation_on_road > road.get("max_wading_depth_m", 0.35)

            if is_severed:
                severed_roads.append(road_id)

            road_statuses.append({
                "road_id": road_id,
                "name": road["name"],
                "type": road["type"],
                "inundation_depth_m": round(inundation_on_road, 2),
                "is_severed": is_severed,
                "coordinates": road["coordinates"],
                "connects": road.get("connects", [])
            })

        # 4. Directed Topological Cascade Propagation
        # Pass 1: Power Grid Dependency Propagation
        for node_id, info in node_states.items():
            # If already physically destroyed, skip
            if info["state"] == "FAILED":
                continue

            # Check incoming power suppliers
            in_edges = self.graph.in_edges(node_id, data=True)
            power_suppliers = [u for u, v, d in in_edges if d.get("type") == "POWER"]

            if power_suppliers:
                all_power_dead = all(self.graph.nodes[u]["state"] == "FAILED" for u in power_suppliers)
                if all_power_dead:
                    # Node has lost grid electricity!
                    backup_hours = info["backup_hours_remaining"]

                    # Check if mitigation added a high-capacity mobile DG set
                    if f"DEPLOY_DG_{node_id}" in active_mitigations:
                        backup_hours += 24.0
                        info["backup_hours_remaining"] = backup_hours

                    if backup_hours > 0:
                        # Running on backup generator
                        # Deplete backup hours if storm has been ongoing after landfall
                        hours_on_gen = max(0, t_offset + 4)  # Assume grid lost around T-4h
                        remaining_fuel = max(0.0, backup_hours - (hours_on_gen * 0.8))
                        info["backup_hours_remaining"] = round(remaining_fuel, 1)

                        if remaining_fuel > 0:
                            info["state"] = "DEGRADED"
                            info["failure_cause"] = "RUNNING_ON_BACKUP_GENERATOR"
                        else:
                            info["state"] = "FAILED"
                            info["failure_cause"] = "GRID_POWER_LOSS"
                    else:
                        info["state"] = "FAILED"
                        info["failure_cause"] = "GRID_POWER_LOSS"

                    self.graph.nodes[node_id]["state"] = info["state"]
                    self.graph.nodes[node_id]["failure_cause"] = info["failure_cause"]

        # Pass 2: Water Supply & Emergency Access Severance
        for node_id, info in node_states.items():
            if info["type"] == "HOSPITAL" and info["state"] != "FAILED":
                # Check water supply
                in_edges = self.graph.in_edges(node_id, data=True)
                water_suppliers = [u for u, v, d in in_edges if d.get("type") == "WATER"]
                if water_suppliers:
                    all_water_dead = all(self.graph.nodes[u]["state"] == "FAILED" for u in water_suppliers)
                    if all_water_dead:
                        if info["state"] == "OPERATIONAL":
                            info["state"] = "DEGRADED"
                            info["failure_cause"] = "WATER_SUPPLY_SEVERED"

                # Check road accessibility to fuel reserves
                # If connecting highway is severed, hospital is isolated
                if node_id == "HOSP_PURI_DHH" and "ROAD_NH316_PURI" in severed_roads:
                    info["isolated_from_resupply"] = True
                elif node_id == "HOSP_PARADIP_PORT" and "ROAD_NH53_PARADIP" in severed_roads:
                    info["isolated_from_resupply"] = True

        # 5. Compute Systemic Resilience Metrics & Cascading Impact
        operational_count = sum(1 for n in node_states.values() if n["state"] == "OPERATIONAL")
        degraded_count = sum(1 for n in node_states.values() if n["state"] == "DEGRADED")
        failed_count = sum(1 for n in node_states.values() if n["state"] == "FAILED")

        critical_hospitals_at_risk = [
            n["name"] for n in node_states.values()
            if n["type"] == "HOSPITAL" and (n["state"] in ["DEGRADED", "FAILED"] or n["isolated_from_resupply"])
        ]

        de_energized_substations = [
            n["name"] for n in node_states.values()
            if n["type"] == "SUBSTATION" and n["state"] == "FAILED"
        ]

        # Identify key cut-set: Which failed substation caused the most downstream degradation?
        cutset_impact: Dict[str, int] = {}
        for sub_id in [n["node_id"] for n in node_states.values() if n["type"] == "SUBSTATION" and n["state"] == "FAILED"]:
            downstream = list(nx.descendants(self.graph, sub_id))
            impacted = sum(1 for d in downstream if node_states[d]["state"] != "OPERATIONAL")
            cutset_impact[sub_id] = impacted

        most_critical_cutset_id = max(cutset_impact, key=cutset_impact.get) if cutset_impact else None
        most_critical_cutset_name = (
            node_states[most_critical_cutset_id]["name"] if most_critical_cutset_id else "None"
        )

        return {
            "t_offset_hours": t_offset,
            "cyclone_eye": {"lat": eye_lat, "lon": eye_lon},
            "p_central_hpa": p_central,
            "max_wind_kmph": max_wind,
            "summary_metrics": {
                "total_assets": len(node_states),
                "operational_count": operational_count,
                "degraded_count": degraded_count,
                "failed_count": failed_count,
                "severed_road_corridors_count": len(severed_roads),
                "most_critical_cutset": most_critical_cutset_name,
                "critical_hospitals_at_risk": critical_hospitals_at_risk,
                "de_energized_substations": de_energized_substations
            },
            "nodes": list(node_states.values()),
            "roads": road_statuses,
            "active_mitigations": active_mitigations
        }
