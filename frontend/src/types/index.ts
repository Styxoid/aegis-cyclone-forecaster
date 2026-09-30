export type NodeState = "OPERATIONAL" | "DEGRADED" | "FAILED";
export type NodeCriticality = "P0_LIFE_CRITICAL" | "P1_INFRA_BACKBONE" | "P2_LOGISTICS" | "P3_CIVIC_SHELTER";
export type FailureCause = "NONE" | "DIRECT_WIND" | "SURGE_INUNDATION" | "GRID_POWER_LOSS" | "WATER_SUPPLY_SEVERED" | "RUNNING_ON_BACKUP_GENERATOR";

export interface CycloneTrackPoint {
  step_id: number;
  t_offset_hours: number;
  timestamp_utc: string;
  latitude: number;
  longitude: number;
  central_pressure_hpa: number;
  max_sustained_wind_kmph: number;
  radius_max_winds_km: number;
  forward_speed_kmph: number;
  bearing_degrees: number;
  category: string;
  description: string;
}

export interface InfrastructureNode {
  node_id: string;
  name: string;
  type: "SUBSTATION" | "HOSPITAL" | "WATER_PUMP" | "SHELTER" | "FUEL_DEPOT";
  lat: number;
  lon: number;
  district: string;
  criticality: NodeCriticality;
  current_wind_speed_kmph: number;
  current_surge_depth_m: number;
  state: NodeState;
  failure_cause: FailureCause;
  backup_hours_remaining: number;
  isolated_from_resupply: boolean;
  mitigations_active: string[];
}

export interface RoadStatus {
  road_id: string;
  name: string;
  type: string;
  inundation_depth_m: number;
  is_severed: boolean;
  coordinates: [number, number][];
  connects: string[];
}

export interface InfrastructureEdge {
  source: string;
  target: string;
  type: "POWER" | "WATER" | "ACCESS";
  description: string;
}

export interface MitigationOption {
  id: string;
  name: string;
  target: string;
  description: string;
  deployment_time_hours: number;
}

export interface VernacularBroadcast {
  english: string;
  odia: string;
  hindi: string;
}

export interface TriageDirective {
  directive_id: string;
  urgency: "IMMEDIATE" | "EXPECTED" | "FUTURE";
  category: string;
  target_facility: string;
  failure_mode: string;
  recommended_action: string;
  counterfactual_impact: string;
  vernacular_broadcast: VernacularBroadcast;
}

export interface SimulationSummary {
  total_assets: number;
  operational_count: number;
  degraded_count: number;
  failed_count: number;
  severed_road_corridors_count: number;
  most_critical_cutset: string;
  critical_hospitals_at_risk: string[];
  de_energized_substations: string[];
}

export interface SimulationResponse {
  status: string;
  timeline: {
    t_offset_hours: number;
    timestamp_utc: string;
    category: string;
    description: string;
  };
  cyclone_state: {
    latitude: number;
    longitude: number;
    central_pressure_hpa: number;
    max_sustained_wind_kmph: number;
    radius_max_winds_km: number;
  };
  summary_metrics: SimulationSummary;
  nodes: InfrastructureNode[];
  roads: RoadStatus[];
  active_mitigations: string[];
  triage: {
    engine: string;
    status: string;
    directives: TriageDirective[];
  };
}

export interface ScenarioFaniResponse {
  scenario_id: string;
  name: string;
  target_region: string;
  track: {
    type: "FeatureCollection";
    features: any[];
  };
  assets: {
    type: "FeatureCollection";
    features: any[];
  };
  roads: {
    type: "FeatureCollection";
    features: any[];
  };
  surge_polygons: {
    type: "FeatureCollection";
    features: any[];
  };
  edges: InfrastructureEdge[];
  mitigation_catalog: MitigationOption[];
}
