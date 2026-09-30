import { NextRequest, NextResponse } from "next/server";
import simulationStates from "@/data/simulation_states.json";

const KNOWN_OFFSETS = [-12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12];

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const t_offset = typeof body.t_offset_hours === "number" ? body.t_offset_hours : 0;
    const active_mitigations: string[] = Array.isArray(body.active_mitigations)
      ? body.active_mitigations
      : [];

    // Find nearest known offset
    const nearestOffset = KNOWN_OFFSETS.reduce((prev, curr) =>
      Math.abs(curr - t_offset) < Math.abs(prev - t_offset) ? curr : prev
    );

    const comboKey = `${nearestOffset}__` + active_mitigations.slice().sort().join("__");
    const statesMap = simulationStates as Record<string, any>;

    let result = statesMap[comboKey];
    if (!result) {
      // Fallback to base state without mitigations if exact combo not found
      const baseKey = `${nearestOffset}__`;
      result = statesMap[baseKey] || Object.values(statesMap)[0];
    }

    // Return the simulation state with the requested offset reflected
    const customizedResult = {
      ...result,
      timeline: {
        ...result.timeline,
        t_offset_hours: t_offset,
      },
      active_mitigations,
    };

    return NextResponse.json(customizedResult);
  } catch (error: any) {
    return NextResponse.json(
      { error: "Simulation calculation error", details: error?.message },
      { status: 400 }
    );
  }
}
