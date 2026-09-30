"use client";

import React, { useState, useEffect } from "react";
import { Eye, Sparkles, X, Shield, Cpu, RefreshCw, CheckCircle2 } from "lucide-react";

interface SatelliteTileItem {
  id: string;
  name: string;
  coordinates: [number, number];
  image_url: string;
}

interface SatelliteVisionInspectorProps {
  isOpen: boolean;
  onClose: () => void;
  apiBaseUrl?: string;
}

export const SatelliteVisionInspector: React.FC<SatelliteVisionInspectorProps> = ({
  isOpen,
  onClose,
  apiBaseUrl = ""
}) => {
  const [tiles, setTiles] = useState<SatelliteTileItem[]>([]);
  const [selectedTileId, setSelectedTileId] = useState<string>("PARADIP_SUBSTATION");
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  useEffect(() => {
    if (!isOpen) return;

    async function fetchTiles() {
      try {
        const res = await fetch(`${apiBaseUrl}/api/multimodal/tiles`);
        if (res.ok) {
          const data = await res.json();
          setTiles(data);
        }
      } catch (err) {
        console.error("Failed to load satellite tile list:", err);
      }
    }
    fetchTiles();
  }, [isOpen, apiBaseUrl]);

  useEffect(() => {
    if (!isOpen || !selectedTileId) return;

    async function runAnalysis() {
      try {
        setIsAnalyzing(true);
        const res = await fetch(`${apiBaseUrl}/api/multimodal/inspect-tile`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ tile_id: selectedTileId })
        });
        if (res.ok) {
          const data = await res.json();
          setAnalysisResult(data);
        }
      } catch (err) {
        console.error("Failed to inspect satellite tile:", err);
      } finally {
        setIsAnalyzing(false);
      }
    }
    runAnalysis();
  }, [isOpen, selectedTileId, apiBaseUrl]);

  if (!isOpen) return null;

  const currentTile = tiles.find((t) => t.id === selectedTileId);
  const isGemini = analysisResult?.engine?.includes("GEMINI");

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="relative w-full max-w-4xl bg-zinc-950 border border-zinc-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-850 bg-zinc-900/40">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
              <Eye className="w-4 h-4 text-cyan-400" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-sm font-semibold text-zinc-100 tracking-tight">
                  Multimodal Satellite Vision Inspector
                </h3>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-400 border border-zinc-700">
                  Sentinel-2 Multi-Spectral
                </span>
              </div>
              <p className="text-xs text-zinc-400">
                Gemini 2.0 Flash zero-shot visual reasoning across coastal bio-shields and structural roof materials
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left Column: Tile Selector & Image Display */}
          <div className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-[11px] font-mono text-zinc-400 uppercase tracking-wider">
                Select Coastal Swath Crop
              </label>
              <div className="grid grid-cols-3 gap-2">
                {tiles.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setSelectedTileId(t.id)}
                    className={`p-2 rounded-xl text-left border text-xs transition-all ${
                      selectedTileId === t.id
                        ? "bg-cyan-950/30 border-cyan-500/60 text-cyan-300"
                        : "bg-zinc-900/60 border-zinc-800 text-zinc-400 hover:border-zinc-700"
                    }`}
                  >
                    <div className="font-semibold truncate text-[11px]">{t.name.split(" ")[0]}</div>
                    <div className="text-[9px] text-zinc-500 font-mono">
                      {t.coordinates[1]}°N, {t.coordinates[0]}°E
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Satellite Imagery Frame */}
            <div className="relative aspect-square w-full rounded-xl overflow-hidden border border-zinc-800 bg-zinc-900 flex items-center justify-center group">
              {currentTile ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  src={`${apiBaseUrl}${currentTile.image_url}`}
                  alt={currentTile.name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="text-xs text-zinc-500">Loading satellite raster...</div>
              )}

              {/* Resolution Overlay Badge */}
              <div className="absolute bottom-3 left-3 bg-zinc-950/80 backdrop-blur-md px-2.5 py-1 rounded-md border border-zinc-850 text-[10px] font-mono text-zinc-300">
                Sentinel-2 MSI | Ground Resolution: 10m/px
              </div>
            </div>
          </div>

          {/* Right Column: Multimodal AI Inference & Extraction */}
          <div className="flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-zinc-850">
                <span className="text-xs font-semibold text-zinc-300">
                  Visual Feature Extraction
                </span>
                <div className="flex items-center space-x-1.5 px-2 py-0.5 rounded-full bg-zinc-900 border border-zinc-800 text-[10px] font-mono">
                  {isGemini ? (
                    <>
                      <Sparkles className="w-3 h-3 text-cyan-400" />
                      <span className="text-cyan-300">Gemini 2.0 Flash Vision</span>
                    </>
                  ) : (
                    <>
                      <Cpu className="w-3 h-3 text-emerald-400" />
                      <span className="text-emerald-300">Calibrated Optical Engine</span>
                    </>
                  )}
                </div>
              </div>

              {isAnalyzing ? (
                <div className="py-20 flex flex-col items-center justify-center space-y-2 text-zinc-500 text-xs">
                  <RefreshCw className="w-5 h-5 animate-spin text-cyan-400" />
                  <span>Executing visual feature extraction...</span>
                </div>
              ) : analysisResult ? (
                <div className="mt-4 space-y-3">
                  {/* Gauge Metrics */}
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80">
                      <div className="text-[10px] text-zinc-400 font-mono">Mangrove Bio-Shield</div>
                      <div className="text-sm font-bold text-emerald-400 font-mono mt-0.5">
                        {Math.round((analysisResult.analysis?.bio_shield_density_score || 0.4) * 100)}%
                      </div>
                      <div className="text-[9px] text-zinc-500 mt-1">Canopy attenuation factor</div>
                    </div>

                    <div className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80">
                      <div className="text-[10px] text-zinc-400 font-mono">Roof Vulnerability</div>
                      <div className="text-sm font-bold text-amber-400 font-mono mt-0.5">
                        {analysisResult.analysis?.roof_fragility_multiplier || 1.4}x
                      </div>
                      <div className="text-[9px] text-zinc-500 mt-1">Tin / Thatch multiplier</div>
                    </div>

                    <div className="p-3 rounded-xl bg-zinc-900/60 border border-zinc-800/80">
                      <div className="text-[10px] text-zinc-400 font-mono">Perimeter Drainage Risk</div>
                      <div className="text-sm font-bold text-rose-400 font-mono mt-0.5">
                        {Math.round((analysisResult.analysis?.drainage_choke_probability || 0.6) * 100)}%
                      </div>
                      <div className="text-[9px] text-zinc-500 mt-1">Silt / backflow breach</div>
                    </div>

                    <div className="p-3 rounded-xl bg-cyan-950/20 border border-cyan-500/30">
                      <div className="text-[10px] text-cyan-300 font-mono">Injected Damage Factor</div>
                      <div className="text-sm font-bold text-cyan-300 font-mono mt-0.5">
                        {analysisResult.analysis?.calibrated_fragility_factor || 1.35}
                      </div>
                      <div className="text-[9px] text-cyan-400/80 mt-1">Physics curve calibrated</div>
                    </div>
                  </div>

                  {/* Visual Evidence Rationale */}
                  <div className="p-3 rounded-xl bg-zinc-900/40 border border-zinc-800/60 text-xs">
                    <span className="text-[10px] uppercase font-mono text-zinc-400 block mb-1">
                      Visual Evidence Identified:
                    </span>
                    <p className="text-zinc-300 leading-relaxed text-[11px]">
                      {analysisResult.analysis?.visual_evidence}
                    </p>
                  </div>

                  {/* Tactical Operational Advice */}
                  <div className="p-3 rounded-xl bg-emerald-950/20 border border-emerald-800/40 text-xs flex items-start space-x-2">
                    <Shield className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="text-[10px] uppercase font-mono text-emerald-300 block mb-0.5">
                        Tactical Preemptive Action:
                      </span>
                      <p className="text-emerald-200/90 text-[11px] leading-relaxed">
                        {analysisResult.analysis?.suggested_preemptive_action}
                      </p>
                    </div>
                  </div>
                </div>
              ) : null}
            </div>

            <div className="pt-3 border-t border-zinc-850 flex items-center justify-between text-[11px] text-zinc-400">
              <span className="flex items-center space-x-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400" />
                <span>Calibrated against Copernicus Sentinel-2 MSI L2A</span>
              </span>
              <button
                onClick={onClose}
                className="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium transition-colors"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
