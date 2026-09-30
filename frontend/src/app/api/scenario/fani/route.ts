import { NextResponse } from "next/server";
import scenarioData from "@/data/scenario_fani.json";

export async function GET() {
  return NextResponse.json(scenarioData, {
    headers: {
      "Cache-Control": "public, max-age=3600, s-maxage=86400",
    },
  });
}
