"use client";

import React, { useState, useEffect, useCallback } from "react";
import { AlertCircle, RefreshCw, X } from "lucide-react";
import { ResilienceMetricsBar } from "@/components/ResilienceMetricsBar";
import { ResilienceDeckMap } from "@/components/ResilienceDeckMap";
import { TimeScrubber } from "@/components/TimeScrubber";
import { IncidentDispatchConsole } from "@/components/IncidentDispatchConsole";
import { MitigationDrawer } from "@/components/MitigationDrawer";
import { SatelliteVisionInspector } from "@/components/SatelliteVisionInspector";
import {
  ScenarioFaniResponse,
  SimulationResponse,
  InfrastructureNode
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "";

export default function Home() {
  const [scenarioData, setScenarioData] = useState<ScenarioFaniResponse | null>(null);
  const [simulationState, setSimulationState] = useState<SimulationResponse | null>(null);
  const [currentOffset, setCurrentOffset] = useState<number>(0); // Default to landfall T=0
  const [activeMitigations, setActiveMitigations] = useState<string[]>([]);
  const [isMitigationOpen, setIsMitigationOpen] = useState<boolean>(false);
  const [isSatelliteOpen, setIsSatelliteOpen] = useState<boolean>(false);
  const [isConsoleOpen, setIsConsoleOpen] = useState<boolean>(true);
  const [selectedNode, setSelectedNode] = useState<InfrastructureNode | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // 1. Fetch Baseline Scenario (Fani track, assets, roads, surge contours, mitigation catalog)
  useEffect(() => {
    async function loadScenario() {
      try {
        setIsLoading(true);
        const res = await fetch(`${API_BASE_URL}/api/scenario/fani`);
        if (!res.ok) {
          throw new Error(`Failed to load scenario: HTTP ${res.status}`);
        }
        const data: ScenarioFaniResponse = await res.json();
        setScenarioData(data);
        setErrorMsg(null);
      } catch (err: any) {
        console.error("Scenario load error:", err);
        setErrorMsg(
          "Backend connection offline. Ensure FastAPI server is running on http://127.0.0.1:8000"
        );
      } finally {
        setIsLoading(false);
      }
    }
    loadScenario();
  }, []);

  // 2. Fetch Simulation Step on offset change or mitigation toggle
  const runSimulation = useCallback(
    async (offset: number, mitigations: string[]) => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/simulate/step`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            t_offset_hours: offset,
            active_mitigations: mitigations
          })
        });
        if (!res.ok) {
          throw new Error(`Simulation step failed: HTTP ${res.status}`);
        }
        const data: SimulationResponse = await res.json();
        setSimulationState(data);
        setErrorMsg(null);
      } catch (err: any) {
        console.error("Simulation step error:", err);
      }
    },
    []
  );

  useEffect(() => {
    if (scenarioData) {
      runSimulation(currentOffset, activeMitigations);
    }
  }, [scenarioData, currentOffset, activeMitigations, runSimulation]);

  const handleToggleMitigation = (id: string) => {
    setActiveMitigations((prev) =>
      prev.includes(id) ? prev.filter((m) => m !== id) : [...prev, id]
    );
  };

  const cycloneEye = simulationState
    ? {
        lat: simulationState.cyclone_state.latitude,
        lon: simulationState.cyclone_state.longitude,
        radius_km: simulationState.cyclone_state.radius_max_winds_km
      }
    : null;

  return (
    <main className="relative flex flex-col h-screen w-screen overflow-hidden bg-zinc-950 font-sans">
      {/* 1. Top Minimalist Telemetry & Metrics HUD */}
      <ResilienceMetricsBar
        summary={simulationState?.summary_metrics || null}
        cycloneState={simulationState?.cyclone_state || null}
        category={simulationState?.timeline.category || "Extremely Severe Cyclonic Storm"}
        onOpenSatelliteInspector={() => setIsSatelliteOpen(true)}
        onToggleMitigations={() => setIsMitigationOpen(!isMitigationOpen)}
        isMitigationActive={isMitigationOpen || activeMitigations.length > 0}
        activeMitigationCount={activeMitigations.length}
        isConsoleOpen={isConsoleOpen}
        onToggleConsole={() => setIsConsoleOpen(!isConsoleOpen)}
      />

      {/* Loading Overlay */}
      {isLoading && (
        <div className="bg-zinc-900/90 text-cyan-300 px-4 py-1 text-xs flex items-center justify-center space-x-2 border-b border-zinc-800 z-50">
          <RefreshCw className="w-3 h-3 animate-spin text-cyan-400" />
          <span>Synchronizing spatial layers...</span>
        </div>
      )}

      {/* Backend Disconnection Banner */}
      {errorMsg && (
        <div className="bg-rose-950/90 text-rose-200 px-4 py-2 text-xs flex items-center justify-between border-b border-rose-800 z-50">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <span>{errorMsg}</span>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="flex items-center space-x-1 px-2 py-0.5 bg-rose-900 hover:bg-rose-850 rounded text-white text-[11px]"
          >
            <RefreshCw className="w-3 h-3" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* 2. Main Visual Canvas Area */}
      <div className="relative flex-1 flex overflow-hidden">
        {/* WebGL 3D Deck.gl Canvas */}
        <div className="flex-1 relative h-full w-full">
          <ResilienceDeckMap
            surgePolygons={scenarioData?.surge_polygons || null}
            trackGeojson={scenarioData?.track || null}
            nodes={simulationState?.nodes || []}
            roads={simulationState?.roads || []}
            edges={scenarioData?.edges || []}
            cycloneEye={cycloneEye}
            onNodeSelect={(node) => setSelectedNode(node)}
          />

          {/* Mitigation Lab Drawer Modal */}
          <MitigationDrawer
            catalog={scenarioData?.mitigation_catalog || []}
            activeMitigations={activeMitigations}
            onToggleMitigation={handleToggleMitigation}
            isOpen={isMitigationOpen}
            onClose={() => setIsMitigationOpen(false)}
          />

          {/* Multimodal Satellite Vision Inspector Modal */}
          <SatelliteVisionInspector
            isOpen={isSatelliteOpen}
            onClose={() => setIsSatelliteOpen(false)}
            apiBaseUrl={API_BASE_URL}
          />

          {/* Detailed Node Inspector Modal (On Map Node Click) */}
          {selectedNode && (
            <div className="absolute top-16 left-4 w-80 bg-zinc-950/95 backdrop-blur-xl border border-zinc-800 rounded-xl p-4 text-zinc-100 shadow-2xl z-30 space-y-3 animate-in fade-in duration-150">
              <div className="flex items-center justify-between border-b border-zinc-850 pb-2">
                <div>
                  <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider">
                    {selectedNode.type}
                  </span>
                  <h3 className="font-semibold text-xs text-zinc-200">
                    {selectedNode.name}
                  </h3>
                </div>
                <button
                  onClick={() => setSelectedNode(null)}
                  className="p-1 rounded text-zinc-400 hover:text-zinc-100 hover:bg-zinc-850"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="space-y-1.5 text-xs font-mono">
                <div className="flex justify-between py-1 border-b border-zinc-900">
                  <span className="text-zinc-500">State:</span>
                  <span
                    className={`font-semibold px-2 py-0.5 rounded text-[10px] ${
                      selectedNode.state === "OPERATIONAL"
                        ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        : selectedNode.state === "DEGRADED"
                        ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                    }`}
                  >
                    {selectedNode.state}
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-zinc-900">
                  <span className="text-zinc-500">Trigger:</span>
                  <span className="text-zinc-300">{selectedNode.failure_cause}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-zinc-900">
                  <span className="text-zinc-500">Surface Wind:</span>
                  <span className="text-rose-400 font-semibold">{selectedNode.current_wind_speed_kmph} km/h</span>
                </div>
                <div className="flex justify-between py-1 border-b border-zinc-900">
                  <span className="text-zinc-500">Surge Depth:</span>
                  <span className="text-cyan-400 font-semibold">{selectedNode.current_surge_depth_m} m</span>
                </div>
                <div className="flex justify-between py-1 border-b border-zinc-900">
                  <span className="text-zinc-500">Backup Generator:</span>
                  <span className="text-amber-400 font-semibold">{selectedNode.backup_hours_remaining} hrs</span>
                </div>
                {selectedNode.isolated_from_resupply && (
                  <div className="p-2 rounded bg-rose-950/20 border border-rose-800/30 text-[11px] text-rose-300 font-sans">
                    Logistics access highway severed. Fuel replenishment impossible.
                  </div>
                )}
              </div>
            </div>
          )}

          {/* 3. Floating Minimalist Timeline Scrubber */}
          <TimeScrubber
            currentOffset={currentOffset}
            onOffsetChange={(offset) => setCurrentOffset(offset)}
            timestampUtc={simulationState?.timeline.timestamp_utc || ""}
            narrativeDescription={simulationState?.timeline.description || ""}
          />
        </div>

        {/* 4. Collapsible Incident Command Drawer */}
        <IncidentDispatchConsole
          directives={simulationState?.triage.directives || []}
          engineName={simulationState?.triage.engine || "HEURISTIC_ENGINE"}
          isOpen={isConsoleOpen}
        />
      </div>
    </main>
  );
}
