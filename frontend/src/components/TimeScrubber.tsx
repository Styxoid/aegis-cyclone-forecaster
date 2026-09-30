"use client";

import React, { useEffect, useState } from "react";
import { Play, Pause, SkipBack, SkipForward, Clock } from "lucide-react";

interface TimeScrubberProps {
  currentOffset: number;
  onOffsetChange: (offset: number) => void;
  timestampUtc: string;
  narrativeDescription: string;
}

const OFFSETS = [-12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12];

export const TimeScrubber: React.FC<TimeScrubberProps> = ({
  currentOffset,
  onOffsetChange,
  timestampUtc,
  narrativeDescription
}) => {
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    if (isPlaying) {
      interval = setInterval(() => {
        const currentIndex = OFFSETS.indexOf(currentOffset);
        if (currentIndex < OFFSETS.length - 1) {
          onOffsetChange(OFFSETS[currentIndex + 1]);
        } else {
          onOffsetChange(OFFSETS[0]);
        }
      }, 1800);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, currentOffset, onOffsetChange]);

  const handleStep = (direction: "prev" | "next") => {
    const currentIndex = OFFSETS.indexOf(currentOffset);
    if (direction === "prev" && currentIndex > 0) {
      onOffsetChange(OFFSETS[currentIndex - 1]);
    } else if (direction === "next" && currentIndex < OFFSETS.length - 1) {
      onOffsetChange(OFFSETS[currentIndex + 1]);
    }
  };

  const formatOffsetLabel = (offset: number) => {
    if (offset === 0) return "T = 00:00 (Landfall)";
    if (offset < 0) return `T - ${Math.abs(offset).toString().padStart(2, "0")}:00h`;
    return `T + ${offset.toString().padStart(2, "0")}:00h`;
  };

  return (
    <div className="absolute bottom-6 left-1/2 -translate-x-1/2 w-[92%] max-w-2xl bg-zinc-950/80 backdrop-blur-xl border border-zinc-800/80 rounded-2xl px-4 py-3 text-zinc-100 shadow-2xl z-20 select-none">
      {/* Upper Status Line */}
      <div className="flex items-center justify-between text-[11px] mb-2 px-1">
        <div className="flex items-center space-x-2">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span className="font-mono font-semibold text-cyan-300">
            {formatOffsetLabel(currentOffset)}
          </span>
          <span className="text-zinc-600">|</span>
          <span className="font-mono text-zinc-400">
            {timestampUtc ? new Date(timestampUtc).toUTCString().replace("GMT", "UTC") : "2019-05-03 03:00 UTC"}
          </span>
        </div>

        <div className="text-zinc-400 italic truncate max-w-xs text-right">
          {narrativeDescription || "Approaching Odisha coast..."}
        </div>
      </div>

      {/* Control Bar & Slider */}
      <div className="flex items-center space-x-3">
        {/* Playback Buttons */}
        <div className="flex items-center space-x-1">
          <button
            onClick={() => handleStep("prev")}
            disabled={currentOffset <= -12}
            className="p-1.5 rounded-lg bg-zinc-900 hover:bg-zinc-850 text-zinc-400 hover:text-zinc-200 disabled:opacity-30 transition-colors"
            title="Step Back 2 Hours"
          >
            <SkipBack className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`p-2 rounded-xl transition-all shadow-md ${
              isPlaying
                ? "bg-amber-400 text-zinc-950 hover:bg-amber-300"
                : "bg-cyan-500 text-zinc-950 hover:bg-cyan-400"
            }`}
            title={isPlaying ? "Pause Simulation" : "Auto-Play Timeline"}
          >
            {isPlaying ? (
              <Pause className="w-3.5 h-3.5 fill-current" />
            ) : (
              <Play className="w-3.5 h-3.5 fill-current" />
            )}
          </button>

          <button
            onClick={() => handleStep("next")}
            disabled={currentOffset >= 12}
            className="p-1.5 rounded-lg bg-zinc-900 hover:bg-zinc-850 text-zinc-400 hover:text-zinc-200 disabled:opacity-30 transition-colors"
            title="Step Forward 2 Hours"
          >
            <SkipForward className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Minimal Range Track */}
        <div className="flex-1 relative flex items-center px-1">
          <input
            type="range"
            min={-12}
            max={12}
            step={2}
            value={currentOffset}
            onChange={(e) => onOffsetChange(parseInt(e.target.value, 10))}
            className="w-full h-1.5 bg-zinc-850 rounded-lg appearance-none cursor-pointer accent-cyan-400 focus:outline-none"
          />
        </div>

        {/* Milestone Quick Jump Buttons */}
        <div className="hidden sm:flex items-center space-x-1 font-mono text-[10px]">
          <button
            onClick={() => onOffsetChange(-12)}
            className={`px-2 py-0.5 rounded transition-colors ${
              currentOffset === -12
                ? "bg-cyan-500 text-zinc-950 font-bold"
                : "bg-zinc-900 hover:bg-zinc-850 text-zinc-400"
            }`}
          >
            -12h
          </button>
          <button
            onClick={() => onOffsetChange(-4)}
            className={`px-2 py-0.5 rounded transition-colors ${
              currentOffset === -4
                ? "bg-amber-400 text-zinc-950 font-bold"
                : "bg-zinc-900 hover:bg-zinc-850 text-zinc-400"
            }`}
          >
            -4h
          </button>
          <button
            onClick={() => onOffsetChange(0)}
            className={`px-2 py-0.5 rounded transition-colors ${
              currentOffset === 0
                ? "bg-rose-500 text-white font-bold"
                : "bg-zinc-900 hover:bg-zinc-850 text-zinc-400"
            }`}
          >
            Landfall
          </button>
          <button
            onClick={() => onOffsetChange(4)}
            className={`px-2 py-0.5 rounded transition-colors ${
              currentOffset === 4
                ? "bg-cyan-500 text-zinc-950 font-bold"
                : "bg-zinc-900 hover:bg-zinc-850 text-zinc-400"
            }`}
          >
            +4h
          </button>
        </div>
      </div>
    </div>
  );
};
