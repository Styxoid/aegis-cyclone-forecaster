"""
vertex_agent.py - Cognitive reasoning and triage service interfacing with Google Gemini.
Integrates Gemini 2.0 / 1.5 Flash for multimodal reasoning, counterfactual evaluation, and multilingual CAP directives.
Guarantees anti-fragile execution: Lazy client initialization with seamless fallback to heuristic_fallback.py.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from services.heuristic_fallback import generate_heuristic_triage_directives

logger = logging.getLogger("AegisSurge.VertexAgent")

_gemini_client = None
_client_initialized = False

def get_gemini_client():
    """
    Safe and lazy initialization of the Google GenAI / Gemini client.
    Does not crash on import or application startup if GEMINI_API_KEY is unset or invalid.
    """
    global _gemini_client, _client_initialized

    if _client_initialized:
        return _gemini_client

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.info("[VertexAgent] GEMINI_API_KEY not detected in environment. Using deterministic heuristic engine.")
        _gemini_client = None
        _client_initialized = True
        return None

    try:
        from google import genai
        _gemini_client = genai.Client(api_key=api_key)
        logger.info("[VertexAgent] Google GenAI Client successfully initialized.")
    except Exception as e:
        logger.warning(f"[VertexAgent] Failed to initialize Gemini client ({e}). Falling back to heuristic engine.")
        _gemini_client = None

    _client_initialized = True
    return _gemini_client

def generate_triage_directives(
    simulation_state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Produces actionable incident command directives and vernacular broadcasts.
    Attempts Gemini reasoning first; if client is unavailable or an error occurs,
    transparently falls back to the deterministic heuristic engine.
    """
    client = get_gemini_client()

    if client is None:
        directives = generate_heuristic_triage_directives(simulation_state)
        return {
            "engine": "DETERMINISTIC_HEURISTIC_FALLBACK",
            "status": "SUCCESS",
            "directives": directives
        }

    try:
        summary = simulation_state.get("summary_metrics", {})
        t_offset = simulation_state.get("t_offset_hours", 0)

        prompt = f"""
You are the Chief Resilience Architect for the Aegis Cyclone Command System.
Analyze this topological infrastructure cascade state for Cyclone Fani at T={t_offset} hours:

Summary Metrics:
- Failed Assets: {summary.get('failed_count')} / {summary.get('total_assets')}
- De-energized Substations: {summary.get('de_energized_substations')}
- Critical Hospitals at Risk: {summary.get('critical_hospitals_at_risk')}
- Cut-Off Highway Corridors: {summary.get('severed_road_corridors_count')}
- Key Network Cut-Set: {summary.get('most_critical_cutset')}

Formulate exactly 3 prioritized, structured incident command directives.
Output must be a strictly valid JSON array of objects with the following schema:
[
  {{
    "directive_id": "DIR_...",
    "urgency": "IMMEDIATE | EXPECTED | FUTURE",
    "category": "ELECTRICAL_GRID_CUTSET | HEALTHCARE_RESILIENCE | CIVIC_EVACUATION",
    "target_facility": "Name of facility",
    "failure_mode": "Concise physical and cascade mechanism",
    "recommended_action": "Tactical operational instruction for district disaster collectors and NDRF battalions",
    "counterfactual_impact": "Quantifiable outcome if action executed vs ignored",
    "vernacular_broadcast": {{
      "english": "Broadcast message",
      "odia": "ସୂଚନା...",
      "hindi": "सूचना..."
    }}
  }}
]
"""
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        )

        raw_text = response.text.strip()
        directives = json.loads(raw_text)

        return {
            "engine": "GEMINI_2_0_FLASH",
            "status": "SUCCESS",
            "directives": directives
        }

    except Exception as exc:
        logger.warning(f"[VertexAgent] Gemini inference encountered error: {exc}. Seamlessly engaging fallback.")
        directives = generate_heuristic_triage_directives(simulation_state)
        return {
            "engine": "DETERMINISTIC_HEURISTIC_FALLBACK",
            "status": "SUCCESS_FALLBACK",
            "error_reason": str(exc),
            "directives": directives
        }
