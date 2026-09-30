-- ==============================================================================
-- AegisSurge: BigQuery GIS Spatial Infrastructure & Hazard Schemas
-- Google Cloud Build with AI: Code for Communities (Track 05: Resilience)
-- Target Region: Odisha Coastal Corridor (Puri, Jagatsinghpur, Khordha)
-- ==============================================================================

-- 1. Table: Critical Infrastructure Assets
-- Clustered by GEOGRAPHY (geom) for sub-second spatial range queries
CREATE OR REPLACE TABLE `aegissurge_prod.infrastructure_assets` (
  asset_id STRING NOT NULL,
  name STRING NOT NULL,
  asset_type STRING NOT NULL, -- 'SUBSTATION', 'HOSPITAL', 'WATER_PUMP', 'SHELTER', 'FUEL_DEPOT'
  district STRING NOT NULL,
  plinth_height_m FLOAT64 NOT NULL,
  wind_threshold_kmph FLOAT64 NOT NULL,
  capacity_units INT64,
  backup_generator_hours FLOAT64,
  criticality STRING NOT NULL, -- 'P0_LIFE_CRITICAL', 'P1_INFRA_BACKBONE', 'P2_LOGISTICS', 'P3_CIVIC_SHELTER'
  geom GEOGRAPHY NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
CLUSTER BY geom, asset_type;

-- 2. Table: Dynamic Cyclone Track & Forecast Cones
-- Partitioned by forecast_hour and clustered by eye_geom
CREATE OR REPLACE TABLE `aegissurge_prod.cyclone_forecast_track` (
  track_id STRING NOT NULL,
  storm_name STRING NOT NULL,
  forecast_hour INT64 NOT NULL, -- Offset in hours (-12 to +12)
  timestamp_utc TIMESTAMP NOT NULL,
  central_pressure_hpa FLOAT64 NOT NULL,
  max_sustained_wind_kmph FLOAT64 NOT NULL,
  radius_max_winds_km FLOAT64 NOT NULL,
  forward_speed_kmph FLOAT64 NOT NULL,
  bearing_degrees FLOAT64 NOT NULL,
  eye_geom GEOGRAPHY NOT NULL,       -- ST_GeogPoint(lon, lat)
  uncertainty_cone GEOGRAPHY NOT NULL -- ST_Buffer polygon
)
PARTITION BY DATE(timestamp_utc)
CLUSTER BY eye_geom;

-- 3. Table: Arterial Road Logistics Corridors
CREATE OR REPLACE TABLE `aegissurge_prod.road_corridors` (
  road_id STRING NOT NULL,
  name STRING NOT NULL,
  road_type STRING NOT NULL, -- 'HIGHWAY', 'COASTAL_HIGHWAY', 'SECONDARY_ROAD'
  elevation_m FLOAT64 NOT NULL,
  max_wading_depth_m FLOAT64 NOT NULL,
  path_geom GEOGRAPHY NOT NULL
)
CLUSTER BY path_geom;

-- ==============================================================================
-- Production Analytical Spatial Queries
-- ==============================================================================

-- QUERY 1: Real-time Asset Spatial Isolation within Dynamic Eye Corridor (Buffer)
-- Executed whenever IMD issues a revised track coordinate
SELECT 
  asset.asset_id,
  asset.name,
  asset.asset_type,
  asset.criticality,
  asset.plinth_height_m,
  asset.wind_threshold_kmph,
  ROUND(ST_DISTANCE(asset.geom, track.eye_geom) / 1000.0, 2) AS distance_to_eye_km,
  ST_ASTEXT(asset.geom) AS geom_wkt
FROM 
  `aegissurge_prod.infrastructure_assets` AS asset
CROSS JOIN 
  `aegissurge_prod.cyclone_forecast_track` AS track
WHERE 
  track.storm_name = 'FANI'
  AND track.forecast_hour = 0 -- Landfall window
  AND ST_DWITHIN(asset.geom, track.eye_geom, track.radius_max_winds_km * 2500.0) -- Buffer 2.5x Rmax
ORDER BY 
  distance_to_eye_km ASC;

-- QUERY 2: Hydrodynamic Inundation Threat & Plinth Breach Analysis
-- Calculates overland distance to coastline and evaluates potential water level breach
WITH CoastlineBaseline AS (
  SELECT ST_GEOGFROMTEXT('LINESTRING(85.75 19.75, 86.05 19.85, 86.30 20.05, 86.70 20.30)') AS coast_geom
),
AssetProximity AS (
  SELECT
    asset.asset_id,
    asset.name,
    asset.asset_type,
    asset.plinth_height_m,
    ROUND(ST_DISTANCE(asset.geom, coast.coast_geom) / 1000.0, 2) AS dist_to_coast_km
  FROM
    `aegissurge_prod.infrastructure_assets` AS asset,
    CoastlineBaseline AS coast
)
SELECT
  a.asset_id,
  a.name,
  a.asset_type,
  a.plinth_height_m,
  a.dist_to_coast_km,
  -- Deterministic exponential surge dissipation: S_shore * exp(-0.18 * dist_km)
  ROUND(3.50 * EXP(-0.18 * a.dist_to_coast_km), 2) AS estimated_surge_water_m,
  ROUND(GREATEST(0.0, (3.50 * EXP(-0.18 * a.dist_to_coast_km)) - a.plinth_height_m), 2) AS inundation_depth_m,
  CASE 
    WHEN (3.50 * EXP(-0.18 * a.dist_to_coast_km)) > a.plinth_height_m THEN 'BREACH_IMMINENT'
    ELSE 'SAFE'
  END AS plinth_status
FROM
  AssetProximity AS a
ORDER BY
  inundation_depth_m DESC;

-- QUERY 3: Road Corridor Severance & Evacuation Cut-Sets
-- Intersects road line strings with discrete storm surge polygons to locate cut points
SELECT
  road.road_id,
  road.name AS road_name,
  road.elevation_m,
  surge.severity AS surge_severity,
  surge.surge_level_m,
  ROUND(GREATEST(0.0, surge.surge_level_m - road.elevation_m), 2) AS water_over_road_m,
  ST_ASTEXT(ST_INTERSECTION(road.path_geom, surge.contour_geom)) AS cut_point_geom
FROM
  `aegissurge_prod.road_corridors` AS road
CROSS JOIN
  `aegissurge_prod.discrete_surge_contours` AS surge
WHERE
  ST_INTERSECTS(road.path_geom, surge.contour_geom)
  AND (surge.surge_level_m - road.elevation_m) > road.max_wading_depth_m;
