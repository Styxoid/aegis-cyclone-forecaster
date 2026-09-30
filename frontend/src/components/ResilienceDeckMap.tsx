"use client";

import React, { useState, useMemo } from "react";
import DeckGL from "@deck.gl/react";
import MapGL from "react-map-gl/maplibre";
import { GeoJsonLayer, PathLayer, ScatterplotLayer, ArcLayer } from "@deck.gl/layers";
import { CARTO_DARK_RASTER_STYLE, INITIAL_VIEW_STATE } from "./MapConfig";
import { InfrastructureNode, RoadStatus, InfrastructureEdge } from "@/types";

interface ResilienceDeckMapProps {
  surgePolygons: any;
  trackGeojson: any;
  nodes: InfrastructureNode[];
  roads: RoadStatus[];
  edges: InfrastructureEdge[];
  cycloneEye: { lat: number; lon: number; radius_km?: number } | null;
  onNodeSelect?: (node: InfrastructureNode) => void;
}

export const ResilienceDeckMap: React.FC<ResilienceDeckMapProps> = ({
  surgePolygons,
  trackGeojson,
  nodes,
  roads,
  edges,
  cycloneEye,
  onNodeSelect
}) => {
  const [hoverInfo, setHoverInfo] = useState<any>(null);

  // Map of node_id -> node for edge coordinate lookup
  const nodeLookup = useMemo(() => {
    const map = new Map<string, InfrastructureNode>();
    nodes.forEach((n) => map.set(n.node_id, n));
    return map;
  }, [nodes]);

  // Enriched edges with coordinates and failure status
  const enrichedEdges = useMemo(() => {
    return edges
      .map((edge) => {
        const src = nodeLookup.get(edge.source);
        const tgt = nodeLookup.get(edge.target);
        if (!src || !tgt) return null;

        const isSourceFailed = src.state === "FAILED";
        return {
          ...edge,
          sourceLon: src.lon,
          sourceLat: src.lat,
          targetLon: tgt.lon,
          targetLat: tgt.lat,
          isSourceFailed
        };
      })
      .filter(Boolean);
  }, [edges, nodeLookup]);

  // Extract track line coordinates
  const trackLineData = useMemo(() => {
    if (!trackGeojson || !trackGeojson.features) return [];
    const lineFeat = trackGeojson.features.find((f: any) => f.geometry.type === "LineString");
    return lineFeat ? [{ path: lineFeat.geometry.coordinates }] : [];
  }, [trackGeojson]);

  // Cyclone eye data
  const cycloneEyeData = useMemo(() => {
    if (!cycloneEye) return [];
    return [
      {
        coordinates: [cycloneEye.lon, cycloneEye.lat],
        radiusMeters: (cycloneEye.radius_km || 30) * 1000
      }
    ];
  }, [cycloneEye]);

  // Memoized 60 FPS WebGL Layers
  const layers = useMemo(() => {
    return [
      // 1. 3D Extruded Coastal Storm Surge Inundation Polygons
      new GeoJsonLayer({
        id: "surge-inundation-polygons",
        data: surgePolygons,
        filled: true,
        extruded: true,
        wireframe: true,
        getElevation: (f: any) => (f.properties?.surge_level_m || 1.0) * 250,
        getFillColor: (f: any) => {
          const severity = f.properties?.severity;
          if (severity === "CRITICAL") return [211, 47, 47, 120];
          if (severity === "MEDIUM") return [2, 136, 209, 100];
          return [0, 188, 212, 70];
        },
        getLineColor: [0, 240, 255, 140],
        lineWidthMinPixels: 1.2,
        pickable: false
      }),

      // 2. Road Network Corridors
      new PathLayer({
        id: "road-corridors-layer",
        data: roads,
        getPath: (d: RoadStatus) => d.coordinates,
        getColor: (d: RoadStatus) => (d.is_severed ? [239, 68, 68, 240] : [34, 197, 94, 160]),
        getWidth: (d: RoadStatus) => (d.is_severed ? 6 : 3),
        widthMinPixels: 2.5,
        pickable: true,
        onHover: (info) => setHoverInfo(info)
      }),

      // 3. Topological Dependency Arcs
      new ArcLayer({
        id: "topological-dependency-arcs",
        data: enrichedEdges,
        getSourcePosition: (d: any) => [d.sourceLon, d.sourceLat],
        getTargetPosition: (d: any) => [d.targetLon, d.targetLat],
        getSourceColor: (d: any) => (d.isSourceFailed ? [239, 68, 68, 220] : [0, 255, 255, 180]),
        getTargetColor: (d: any) => (d.isSourceFailed ? [245, 158, 11, 220] : [34, 197, 94, 180]),
        getWidth: (d: any) => (d.isSourceFailed ? 4 : 2),
        getHeight: 0.5,
        pickable: true,
        onHover: (info) => setHoverInfo(info)
      }),

      // 4. Cyclone Full Track Line
      new PathLayer({
        id: "cyclone-track-line",
        data: trackLineData,
        getPath: (d: any) => d.path,
        getColor: [0, 229, 255, 140],
        getWidth: 2.5,
        widthMinPixels: 2
      }),

      // 5. Cyclone Eye & Radius of Maximum Winds
      new ScatterplotLayer({
        id: "cyclone-rmax-circle",
        data: cycloneEyeData,
        getPosition: (d: any) => d.coordinates,
        getRadius: (d: any) => d.radiusMeters,
        getFillColor: [239, 68, 68, 25],
        getLineColor: [239, 68, 68, 180],
        lineWidthMinPixels: 2,
        stroked: true,
        filled: true
      }),

      // 6. Cyclone Eye Core
      new ScatterplotLayer({
        id: "cyclone-eye-core",
        data: cycloneEyeData,
        getPosition: (d: any) => d.coordinates,
        getRadius: 5000,
        getFillColor: [255, 255, 255, 220],
        getLineColor: [239, 68, 68, 240],
        lineWidthMinPixels: 2.5,
        stroked: true,
        filled: true
      }),

      // 7. Critical Infrastructure Nodes
      new ScatterplotLayer({
        id: "infrastructure-nodes-layer",
        data: nodes,
        getPosition: (d: InfrastructureNode) => [d.lon, d.lat],
        getRadius: (d: InfrastructureNode) =>
          d.criticality === "P0_LIFE_CRITICAL" ? 1600 : 1100,
        getFillColor: (d: InfrastructureNode) => {
          if (d.state === "FAILED") return [239, 68, 68, 240];
          if (d.state === "DEGRADED") return [245, 158, 11, 240];
          return [34, 197, 94, 240];
        },
        getLineColor: [255, 255, 255, 220],
        lineWidthMinPixels: 2,
        stroked: true,
        filled: true,
        pickable: true,
        onClick: (info) => {
          if (info.object && onNodeSelect) {
            onNodeSelect(info.object as InfrastructureNode);
          }
        },
        onHover: (info) => setHoverInfo(info)
      })
    ];
  }, [surgePolygons, roads, enrichedEdges, trackLineData, cycloneEyeData, nodes, onNodeSelect]);

  return (
    <div className="relative w-full h-full bg-zinc-950 overflow-hidden">
      <DeckGL
        initialViewState={INITIAL_VIEW_STATE}
        controller={true}
        layers={layers}
      >
        <MapGL
          mapStyle={CARTO_DARK_RASTER_STYLE as any}
          reuseMaps
          attributionControl={false}
        />
      </DeckGL>

      {/* Minimal Map Legend */}
      <div className="absolute top-4 left-4 bg-zinc-950/80 backdrop-blur-md border border-zinc-800 rounded-xl px-3 py-2.5 text-[11px] text-zinc-300 z-20 space-y-1.5 shadow-xl select-none">
        <div className="font-mono text-[9px] uppercase tracking-widest text-zinc-500 pb-1 border-b border-zinc-850">
          Node Telemetry
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
          <span>Nominal</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-amber-400" />
          <span>Generator Mode</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-rose-400" />
          <span>Tripped / Flooded</span>
        </div>
        <div className="flex items-center space-x-2 pt-1 border-t border-zinc-850 text-[10px] text-zinc-400">
          <span className="w-3 h-0.5 bg-cyan-400 rounded-full" />
          <span>Active Flow Arc</span>
        </div>
      </div>

      {/* Sleek Tooltip */}
      {hoverInfo && hoverInfo.object && (
        <div
          className="pointer-events-none absolute z-50 bg-zinc-950/90 backdrop-blur-xl border border-zinc-800 rounded-xl p-3 text-xs text-zinc-100 shadow-2xl max-w-xs"
          style={{ left: hoverInfo.x + 15, top: hoverInfo.y + 15 }}
        >
          {hoverInfo.object.node_id ? (
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-zinc-200">{hoverInfo.object.name}</span>
                <span
                  className={`text-[9px] font-mono px-1.5 py-0.2 rounded font-semibold ${
                    hoverInfo.object.state === "OPERATIONAL"
                      ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                      : hoverInfo.object.state === "DEGRADED"
                      ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                      : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                  }`}
                >
                  {hoverInfo.object.state}
                </span>
              </div>
              <div className="text-[10px] text-zinc-400 font-mono">
                {hoverInfo.object.type} | {hoverInfo.object.district}
              </div>
              <div className="grid grid-cols-2 gap-1 text-[10px] bg-zinc-900/60 p-2 rounded-lg border border-zinc-850 font-mono">
                <div>Wind: <span className="text-rose-300 font-semibold">{hoverInfo.object.current_wind_speed_kmph} km/h</span></div>
                <div>Surge: <span className="text-cyan-300 font-semibold">{hoverInfo.object.current_surge_depth_m} m</span></div>
                <div>Fuel: <span className="text-amber-300 font-semibold">{hoverInfo.object.backup_hours_remaining}h</span></div>
                <div>Trigger: <span className="text-zinc-300">{hoverInfo.object.failure_cause}</span></div>
              </div>
              {hoverInfo.object.isolated_from_resupply && (
                <div className="text-[10px] text-rose-300 bg-rose-950/30 p-1.5 rounded border border-rose-800/30">
                  Highway severed; isolated from fuel replenishment.
                </div>
              )}
            </div>
          ) : hoverInfo.object.road_id ? (
            <div className="space-y-1 font-mono text-[11px]">
              <div className="font-semibold text-zinc-200">{hoverInfo.object.name}</div>
              <div className="text-zinc-400">
                Status:{" "}
                <span className={hoverInfo.object.is_severed ? "text-rose-400 font-semibold" : "text-emerald-400 font-semibold"}>
                  {hoverInfo.object.is_severed ? "SEVERED (Submerged)" : "PASSABLE"}
                </span>
              </div>
              <div className="text-[10px] text-zinc-500">
                Water Depth: {hoverInfo.object.inundation_depth_m}m
              </div>
            </div>
          ) : hoverInfo.object.source ? (
            <div className="space-y-1 font-mono text-[11px]">
              <div className="font-semibold text-zinc-200">{hoverInfo.object.description}</div>
              <div className="text-[10px] text-zinc-400">
                {hoverInfo.object.source} ➔ {hoverInfo.object.target}
              </div>
              <div className="text-[10px]">
                Status:{" "}
                <span className={hoverInfo.object.isSourceFailed ? "text-rose-400 font-semibold" : "text-cyan-400 font-semibold"}>
                  {hoverInfo.object.isSourceFailed ? "GRID CUT" : "ENERGIZED"}
                </span>
              </div>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
};
