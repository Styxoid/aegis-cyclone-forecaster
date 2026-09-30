import { NextResponse } from "next/server";
import multimodalData from "@/data/multimodal_tiles.json";

export async function GET() {
  return NextResponse.json(multimodalData.tiles);
}
