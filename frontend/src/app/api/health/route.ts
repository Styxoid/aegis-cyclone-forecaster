import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    service: "Aegis Next.js Resilience Core",
    version: "1.0.0",
    deployment: "Vercel Edge/Serverless Ready",
  });
}
