import { NextRequest, NextResponse } from "next/server";
import multimodalData from "@/data/multimodal_tiles.json";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const tile_id = body.tile_id;
    const detailsMap = multimodalData.details as Record<string, any>;

    const tile = detailsMap[tile_id];
    if (!tile) {
      return NextResponse.json({ error: "Tile not found" }, { status: 404 });
    }

    return NextResponse.json({
      tile_id,
      name: tile.name,
      engine: "Deterministic Sentinel-2 Visual Intelligence Core (Gemini Fallback)",
      metrics: tile.default_metrics,
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: "Inspection error", details: error?.message },
      { status: 400 }
    );
  }
}
