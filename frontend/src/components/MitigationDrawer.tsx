"use client";

import React from "react";
import { Shield, CheckCircle2, SlidersHorizontal, Sparkles, X } from "lucide-react";
import { MitigationOption } from "@/types";

interface MitigationDrawerProps {
  catalog: MitigationOption[];
  activeMitigations: string[];
  onToggleMitigation: (mitigationId: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

export const MitigationDrawer: React.FC<MitigationDrawerProps> = ({
  catalog,
  activeMitigations,
  onToggleMitigation,
  isOpen,
  onClose
}) => {
  if (!isOpen) return null;

  return (
    <div className="absolute top-16 right-6 w-96 bg-zinc-950/95 backdrop-blur-xl border border-zinc-800 rounded-2xl shadow-2xl p-5 text-zinc-100 z-30 select-none animate-in fade-in slide-in-from-top-2 duration-150">
      <div className="flex items-center justify-between pb-3 border-b border-zinc-850 mb-3">
        <div className="flex items-center space-x-2">
          <SlidersHorizontal className="w-4 h-4 text-cyan-400" />
          <h3 className="font-semibold text-xs tracking-wider uppercase font-mono text-zinc-200">
            Counterfactual Mitigation Lab
          </h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-md text-zinc-400 hover:text-zinc-100 hover:bg-zinc-850 transition-colors"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>

      <p className="text-[11px] text-zinc-400 mb-4 leading-relaxed">
        Toggle hypothetical engineering interventions. The NetworkX cascade solver dynamically recalculates network cut-sets in real-time.
      </p>

      <div className="space-y-2.5">
        {catalog.map((item) => {
          const isActive = activeMitigations.includes(item.id);
          return (
            <div
              key={item.id}
              onClick={() => onToggleMitigation(item.id)}
              className={`p-3 rounded-xl border cursor-pointer transition-all ${
                isActive
                  ? "bg-cyan-950/20 border-cyan-500/60 shadow-sm"
                  : "bg-zinc-900/40 border-zinc-800/80 hover:border-zinc-700"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <Shield
                    className={`w-3.5 h-3.5 flex-shrink-0 ${
                      isActive ? "text-cyan-400" : "text-zinc-500"
                    }`}
                  />
                  <h4 className="text-xs font-semibold text-zinc-200 leading-snug">
                    {item.name}
                  </h4>
                </div>
                <div
                  className={`w-4 h-4 rounded-md border flex items-center justify-center transition-colors flex-shrink-0 ml-2 ${
                    isActive
                      ? "bg-cyan-500 border-cyan-400 text-zinc-950"
                      : "border-zinc-700 bg-zinc-900"
                  }`}
                >
                  {isActive && <CheckCircle2 className="w-3 h-3 stroke-[3]" />}
                </div>
              </div>

              <p className="text-[11px] text-zinc-400 mt-1.5 leading-snug">
                {item.description}
              </p>

              <div className="mt-2 flex items-center justify-between text-[10px] text-zinc-500 font-mono">
                <span>Target: {item.target}</span>
                <span>Deploy: {item.deployment_time_hours}h</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-3.5 p-2.5 rounded-lg bg-zinc-900/60 border border-zinc-850 flex items-center justify-between text-[11px] text-cyan-300 font-mono">
        <span className="flex items-center space-x-1.5">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          <span>Active Interventions:</span>
        </span>
        <strong className="text-cyan-400">{activeMitigations.length} Applied</strong>
      </div>
    </div>
  );
};
