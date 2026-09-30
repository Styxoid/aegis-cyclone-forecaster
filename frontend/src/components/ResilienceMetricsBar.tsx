"use client";

import React from "react";
import { Compass, Eye, SlidersHorizontal, PanelRightClose, PanelRightOpen } from "lucide-react";
import { SimulationSummary } from "@/types";

interface ResilienceMetricsBarProps {
  summary: SimulationSummary | null;
  cycloneState: {
    latitude?: number;
    longitude?: number;
    central_pressure_hpa?: number;
    max_sustained_wind_kmph?: number;
  } | null;
  category: string;
  onOpenSatelliteInspector: () => void;
  onToggleMitigations: () => void;
  isMitigationActive: boolean;
  activeMitigationCount: number;
  isConsoleOpen: boolean;
  onToggleConsole: () => void;
}

export const ResilienceMetricsBar: React.FC<ResilienceMetricsBarProps> = ({
  summary,
  cycloneState,
  category,
  onOpenSatelliteInspector,
  onToggleMitigations,
  isMitigationActive,
  activeMitigationCount,
  isConsoleOpen,
  onToggleConsole
}) => {
  return (
    <header className="h-12 bg-zinc-950/90 backdrop-blur-md border-b border-zinc-850 px-4 flex items-center justify-between text-zinc-100 z-30 select-none">
      {/* Brand & Track */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 rounded-md bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center">
            <Compass className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <span className="font-semibold text-xs tracking-wider uppercase font-mono bg-gradient-to-r from-zinc-100 via-zinc-200 to-zinc-400 bg-clip-text text-transparent">
            Aegis
          </span>
        </div>

        <div className="h-4 w-px bg-zinc-800" />

        <div className="flex items-center space-x-1.5 text-[11px] text-zinc-400 font-mono">
          <span className="text-zinc-200 font-semibold">ODISHA CORRIDOR</span>
          <span className="text-zinc-600">/</span>
          <span className="text-cyan-400">CYCLONE FANI</span>
        </div>
      </div>

      {/* Telemetry Chips (Minimal Monospace HUD) */}
      <div className="hidden lg:flex items-center space-x-3 text-xs font-mono">
        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-zinc-900/60 border border-zinc-850 text-zinc-300">
          <span className="text-zinc-400 text-[10px] uppercase">Class:</span>
          <span className="text-amber-400 font-semibold">{category?.split("(")[0] || "ESCS"}</span>
        </div>

        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-zinc-900/60 border border-zinc-850 text-zinc-300">
          <span className="text-zinc-400 text-[10px] uppercase">Pc:</span>
          <span className="text-cyan-300 font-semibold">{cycloneState?.central_pressure_hpa ?? 932} hPa</span>
        </div>

        <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-md bg-zinc-900/60 border border-zinc-850 text-zinc-300">
          <span className="text-zinc-400 text-[10px] uppercase">Vmax:</span>
          <span className="text-rose-400 font-semibold">{cycloneState?.max_sustained_wind_kmph ?? 215} km/h</span>
        </div>

        <div className="h-4 w-px bg-zinc-800" />

        {/* Status Indicators with Minimal LED Dots */}
        <div className="flex items-center space-x-3 text-[11px]">
          <div className="flex items-center space-x-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 ring-2 ring-emerald-500/20" />
            <span className="text-zinc-400">Nominal:</span>
            <span className="text-emerald-400 font-semibold">{summary?.operational_count ?? 21}</span>
          </div>

          <div className="flex items-center space-x-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 ring-2 ring-amber-500/20" />
            <span className="text-zinc-400">On Gen:</span>
            <span className="text-amber-400 font-semibold">{summary?.degraded_count ?? 0}</span>
          </div>

          <div className="flex items-center space-x-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-400 ring-2 ring-rose-500/20" />
            <span className="text-zinc-400">Failed:</span>
            <span className="text-rose-400 font-semibold">{summary?.failed_count ?? 0}</span>
          </div>

          <div className="flex items-center space-x-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-purple-400 ring-2 ring-purple-500/20" />
            <span className="text-zinc-400">Road Cuts:</span>
            <span className="text-purple-400 font-semibold">{summary?.severed_road_corridors_count ?? 0}</span>
          </div>
        </div>
      </div>

      {/* Action Controls */}
      <div className="flex items-center space-x-2">
        {/* Satellite Vision Inspector Button */}
        <button
          onClick={onOpenSatelliteInspector}
          className="px-2.5 py-1.5 rounded-lg text-xs font-medium flex items-center space-x-1.5 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800 transition-colors"
          title="Inspect Sentinel-2 Multimodal Satellite Tiles"
        >
          <Eye className="w-3.5 h-3.5 text-cyan-400" />
          <span className="hidden sm:inline">Satellite Vision</span>
        </button>

        {/* Counterfactual Mitigation Lab Button */}
        <button
          onClick={onToggleMitigations}
          className={`px-2.5 py-1.5 rounded-lg text-xs font-medium flex items-center space-x-1.5 border transition-all ${
            isMitigationActive
              ? "bg-cyan-950/40 border-cyan-500/70 text-cyan-300"
              : "bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border-zinc-800"
          }`}
          title="Open Counterfactual Mitigation Lab"
        >
          <SlidersHorizontal className="w-3.5 h-3.5 text-cyan-400" />
          <span className="hidden sm:inline">Mitigations</span>
          {activeMitigationCount > 0 && (
            <span className="w-4 h-4 rounded-full bg-cyan-500 text-zinc-950 text-[10px] font-bold flex items-center justify-center font-mono">
              {activeMitigationCount}
            </span>
          )}
        </button>

        <div className="h-4 w-px bg-zinc-800" />

        {/* Toggle Dispatch Console */}
        <button
          onClick={onToggleConsole}
          className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900 transition-colors"
          title={isConsoleOpen ? "Collapse Dispatch Drawer" : "Expand Dispatch Drawer"}
        >
          {isConsoleOpen ? (
            <PanelRightClose className="w-4 h-4" />
          ) : (
            <PanelRightOpen className="w-4 h-4" />
          )}
        </button>
      </div>
    </header>
  );
};
