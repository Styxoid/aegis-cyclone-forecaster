"use client";

import React, { useState, useEffect, useRef } from "react";
import { Radio, AlertCircle, ShieldAlert, Cpu, Sparkles, Volume2, Square, Play } from "lucide-react";
import { TriageDirective } from "@/types";

interface IncidentDispatchConsoleProps {
  directives: TriageDirective[];
  engineName: string;
  isOpen: boolean;
}

export const IncidentDispatchConsole: React.FC<IncidentDispatchConsoleProps> = ({
  directives,
  engineName,
  isOpen
}) => {
  const [selectedLang, setSelectedLang] = useState<"english" | "odia" | "hindi">("english");
  const [playingId, setPlayingId] = useState<string | null>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      synthRef.current = window.speechSynthesis;
    }
    return () => {
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, []);

  const handleStopSpeech = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
    }
    setPlayingId(null);
  };

  const handlePlaySpeech = (directiveId: string, text: string) => {
    if (!synthRef.current) return;

    if (playingId === directiveId) {
      handleStopSpeech();
      return;
    }

    synthRef.current.cancel();
    const utterance = new SpeechSynthesisUtterance(text);

    if (selectedLang === "hindi") {
      utterance.lang = "hi-IN";
    } else if (selectedLang === "odia") {
      utterance.lang = "or-IN";
    } else {
      utterance.lang = "en-IN";
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onend = () => setPlayingId(null);
    utterance.onerror = () => setPlayingId(null);

    setPlayingId(directiveId);
    synthRef.current.speak(utterance);
  };

  if (!isOpen) return null;

  const isGemini = engineName.includes("GEMINI");

  const getUrgencyBadge = (urgency: string) => {
    switch (urgency) {
      case "IMMEDIATE":
        return "bg-rose-500/10 text-rose-400 border-rose-500/20";
      case "EXPECTED":
        return "bg-amber-500/10 text-amber-400 border-amber-500/20";
      default:
        return "bg-cyan-500/10 text-cyan-400 border-cyan-500/20";
    }
  };

  return (
    <aside className="w-80 md:w-96 bg-zinc-950/95 backdrop-blur-xl border-l border-zinc-850 flex flex-col h-full text-zinc-100 z-20 shadow-2xl select-none">
      {/* Header */}
      <div className="p-4 border-b border-zinc-850 bg-zinc-900/30">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Radio className="w-3.5 h-3.5 text-rose-400 animate-pulse" />
            <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-300 font-mono">
              Incident Dispatch Feed
            </h2>
          </div>
          <div className="flex items-center space-x-1.5 px-2 py-0.5 rounded-full bg-zinc-900 border border-zinc-800 text-[10px] font-mono">
            {isGemini ? (
              <>
                <Sparkles className="w-3 h-3 text-cyan-400" />
                <span className="text-cyan-300">Gemini 2.0 Flash</span>
              </>
            ) : (
              <>
                <Cpu className="w-3 h-3 text-emerald-400" />
                <span className="text-emerald-300">Heuristic Engine</span>
              </>
            )}
          </div>
        </div>

        {/* Vernacular Language Selector */}
        <div className="flex items-center space-x-1 bg-zinc-900/80 p-0.5 rounded-lg border border-zinc-800 text-xs">
          <button
            onClick={() => {
              handleStopSpeech();
              setSelectedLang("english");
            }}
            className={`flex-1 py-1 rounded-md text-[11px] font-medium transition-colors ${
              selectedLang === "english"
                ? "bg-zinc-800 text-zinc-100 shadow-sm"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            English
          </button>
          <button
            onClick={() => {
              handleStopSpeech();
              setSelectedLang("odia");
            }}
            className={`flex-1 py-1 rounded-md text-[11px] font-medium transition-colors ${
              selectedLang === "odia"
                ? "bg-zinc-800 text-zinc-100 shadow-sm"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            ଓଡ଼ିଆ
          </button>
          <button
            onClick={() => {
              handleStopSpeech();
              setSelectedLang("hindi");
            }}
            className={`flex-1 py-1 rounded-md text-[11px] font-medium transition-colors ${
              selectedLang === "hindi"
                ? "bg-zinc-800 text-zinc-100 shadow-sm"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            हिन्दी
          </button>
        </div>
      </div>

      {/* Directives Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {directives.length === 0 ? (
          <div className="text-center py-20 text-zinc-500 text-xs">
            Awaiting simulation step telemetry...
          </div>
        ) : (
          directives.map((dir, idx) => {
            const dirId = dir.directive_id || `DIR_${idx}`;
            const broadcastText =
              dir.vernacular_broadcast?.[selectedLang] ||
              dir.vernacular_broadcast?.english ||
              "";
            const isBroadcasting = playingId === dirId;

            return (
              <div
                key={dirId}
                className="bg-zinc-900/40 border border-zinc-800/80 rounded-xl p-3.5 space-y-2.5 hover:border-zinc-700/80 transition-colors"
              >
                {/* Header */}
                <div className="flex items-center justify-between">
                  <span
                    className={`text-[9px] font-mono font-semibold px-2 py-0.5 rounded border ${getUrgencyBadge(
                      dir.urgency
                    )}`}
                  >
                    {dir.urgency}
                  </span>
                  <span className="text-[10px] font-mono text-zinc-400">
                    {dir.category?.replace(/_/g, " ")}
                  </span>
                </div>

                {/* Facility & Failure */}
                <div>
                  <div className="text-xs font-semibold text-zinc-100">
                    {dir.target_facility}
                  </div>
                  <div className="text-[11px] text-zinc-400 mt-0.5 flex items-start space-x-1.5">
                    <AlertCircle className="w-3.5 h-3.5 text-rose-400 flex-shrink-0 mt-0.5" />
                    <span>{dir.failure_mode}</span>
                  </div>
                </div>

                {/* Tactical Action */}
                <div className="bg-zinc-950/70 p-2.5 rounded-lg border border-zinc-850 text-[11px] text-zinc-300 leading-relaxed">
                  <span className="text-cyan-400 font-mono text-[10px] uppercase block mb-1">
                    Tactical Directive:
                  </span>
                  {dir.recommended_action}
                </div>

                {/* Counterfactual Benefit */}
                <div className="text-[10px] text-emerald-400/90 bg-emerald-950/20 border border-emerald-800/30 p-2 rounded-lg flex items-start space-x-1.5">
                  <ShieldAlert className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0 mt-0.5" />
                  <span>
                    <strong className="text-emerald-300">Counterfactual Gain:</strong>{" "}
                    {dir.counterfactual_impact}
                  </span>
                </div>

                {/* Audio Broadcast Box */}
                <div className="bg-zinc-950/80 p-2.5 rounded-lg border border-zinc-850 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-1 text-[10px] text-zinc-400 font-mono uppercase">
                      <Volume2 className="w-3 h-3 text-cyan-400" />
                      <span>CAP Radio Broadcast</span>
                    </div>

                    <button
                      onClick={() => handlePlaySpeech(dirId, broadcastText)}
                      className={`flex items-center space-x-1 px-2 py-0.5 rounded text-[10px] font-medium transition-all ${
                        isBroadcasting
                          ? "bg-rose-500 text-white"
                          : "bg-zinc-800 hover:bg-zinc-750 text-zinc-200 border border-zinc-700"
                      }`}
                      title={isBroadcasting ? "Stop Radio" : "Play Audio Bulletin"}
                    >
                      {isBroadcasting ? (
                        <>
                          <Square className="w-2.5 h-2.5 fill-current" />
                          <span>Stop</span>
                        </>
                      ) : (
                        <>
                          <Play className="w-2.5 h-2.5 fill-current" />
                          <span>Broadcast Audio</span>
                        </>
                      )}
                    </button>
                  </div>

                  {isBroadcasting && (
                    <div className="flex items-center space-x-1.5 py-1 text-[9px] text-cyan-300 font-mono">
                      <div className="flex items-center space-x-0.5">
                        <span className="w-0.5 h-2 bg-cyan-400 animate-pulse" />
                        <span className="w-0.5 h-3.5 bg-cyan-400 animate-pulse delay-75" />
                        <span className="w-0.5 h-1.5 bg-cyan-400 animate-pulse delay-150" />
                        <span className="w-0.5 h-3 bg-cyan-400 animate-pulse delay-100" />
                      </div>
                      <span>Transmitting on Coastal VHF 156.8 MHz & AIR Cuttack...</span>
                    </div>
                  )}

                  <p className="text-[11px] text-zinc-300 leading-relaxed font-sans">
                    {broadcastText}
                  </p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
};
