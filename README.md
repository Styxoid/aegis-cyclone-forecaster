# Aegis: Autonomous Cyclone Impact & Infrastructure Vulnerability Forecaster

[![Google Cloud Build with AI](https://img.shields.io/badge/Google%20Cloud-Build%20with%20AI%202026-4285F4?logo=googlecloud&logoColor=white)](https://hack2skill.com)
[![Track 05](https://img.shields.io/badge/Track%2005-Cyclone%20Resilience-06B6D4)](#)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14%20App%20Router-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Deck.gl](https://img.shields.io/badge/Deck.gl-9.0%20WebGL-red)](https://deck.gl/)
[![Gemini 2.0 Flash](https://img.shields.io/badge/Vertex%20AI-Gemini%202.0%20Flash-8E75C2?logo=google&logoColor=white)](https://cloud.google.com/vertex-ai)

> **Submission for Google Cloud Build with AI: Code for Communities (Second Edition)**  
> **Track 05:** Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster  
> **Theme:** Resilience  
> **Team:** Team GGR  
> **Repository:** [https://github.com/Styxoid/aegis-cyclone-forecaster](https://github.com/Styxoid/aegis-cyclone-forecaster)  

---

## 1. Executive Summary

When a Category 4 or 5 cyclone approaches the Indian coastline (such as Cyclone Fani with 215 km/h winds across Puri and Paradip), disaster response authorities do not lack meteorological weather charts. **They suffer from operational dispatch paralysis caused by unmodeled cross-sector infrastructure dependencies.**

### The Ground Reality Failures:
1. **Coarse Weather Prediction Grids vs. Asset-Level Truth:** Numerical weather models produce 15–25 km grid cells. They cannot predict whether a specific 132/33 kV electrical substation transformer yard with a +1.1m plinth elevation will be submerged by a 1.8m coastal storm surge. Consequently, utilities leave transformers energized until explosive blowout, triggering ₹15Cr+ damage and 6-week regional blackouts.
2. **Abstract Heatmaps vs. Directed Dependency Cascades:** Traditional disaster portals display static flood polygons but fail to model the directed failure cascade:
   $$\text{Substation Flooded} \longrightarrow \text{Water Treatment Halted} \longrightarrow \text{Hospital ICU Fuel Clock (12h)} \longrightarrow \text{Logistics Arterial Road Severed}$$
   Even if a district hospital sits safely on high ground, its life-support generators fail if the arterial highway bridge is impassable to diesel fuel tankers ($>0.35\text{m}$ water depth limit).
3. **IoT Telemetry Blindness:** Coastal anemometers and IoT weather sensors are mechanically sheered and destroyed at 180+ km/h winds, blinding sensor-dependent dashboards at the exact peak of landfall crisis.

**Aegis solves this by anchoring cognitive AI reasoning directly to deterministic atmospheric physics and topological graph cascades.**

---

## 2. Hybrid Triple-Layer Architecture

```
+-------------------------------------------------------------------------------------------------+
|                                        AEGIS HYBRID PARADIGM                                    |
+-------------------------------------------------------------------------------------------------+
|  [ LAYER 1: DETERMINISTIC PHYSICS ]                                                             |
|  * Holland (1980/2010) Parametric Radial Wind Field with Asymmetric Translation Vectors        |
|  * Hydrodynamic Storm Surge Bathymetry (Inverse Barometer Effect + Onshore Wind Setup)          |
|  * Kaplan-DeMaria (1995) Inland Wind Decay Formulation                                          |
|                                       |                                                         |
|                                       v (Physical Forces: Wind km/h, Surge Depth m)             |
|  [ LAYER 2: TOPOLOGICAL GRAPH SOLVER (NetworkX) ]                                               |
|  * Multi-layer Directed Infrastructure Dependency Graph G = (V, E)                              |
|  * Dynamic Edge Severance (Highway corridors marked impassable when water depth > 0.35m)       |
|  * Substation Cut-Sets, Water Intake Shutdowns, and Hospital Generator Runtime Depletions       |
|                                       |                                                         |
|                                       v (Identified Cut-Sets & Bottlenecks)                     |
|  [ LAYER 3: COGNITIVE DISPATCH AGENT (Google Gemini 2.0 Flash) ]                                |
|  * Multimodal Sentinel-2 Satellite Tile Ingestion (Mangrove Density & Roof Fragility Multiplier) |
|  * Counterfactual Resource Rebalancing (Deploying Mobile Generators & Inflatable Flood Berms)   |
|  * Localized Common Alerting Protocol (CAP) Radio Broadcasts in Odia, Hindi, and English        |
+-------------------------------------------------------------------------------------------------+
```

---

## 3. Core Capabilities & Innovation Moat

### The "Zero-Wrapper" AI Moat (25% AI Rubric)
* **ReAct Analytical Tool-Calling:** Gemini 2.0 Flash operates as a strict analytical orchestrator bound to deterministic API tools (`simulate_hydro_wind_decay`, `evaluate_graph_cascade`, `query_infrastructure_cone`, `dispatch_multilingual_cap`). It never invents coordinates or produces hallucinated spatial advice.
* **Multimodal Satellite Vision:** Directly parses high-resolution multi-spectral Sentinel-2 satellite crops, calculating mangrove bio-shield canopy degradation along the Mahanadi estuary and informal roof material vulnerability indices.
* **Anti-Fragile Zero-Downtime Fallback:** If Vertex AI experiences network disconnects, Aegis automatically shifts to an embedded **Deterministic Heuristic Engine** (Dijkstra cut-sets + Betweenness Centrality) in $<5\text{ms}$. The dashboard never hangs.

### Interactive Tactical Command Console (Next.js 14 + WebGL)
* **Hardware-Accelerated 3D WebGL:** 60 FPS rendering using Deck.gl (`GeoJsonLayer`, `PathLayer`, `ArcLayer`) on token-free Esri World Dark Gray basemaps.
* **4D Landfall Timeline Scrubber:** Simulates Cyclone Fani landfall from $T-00:00$ to $T-09:00$ with auto-play, smoothly interpolating hurricane eyewall translation and storm surge polygons.
* **Counterfactual Mitigation Lab:** Emergency managers test proactive interventions (*"What if we erect an inflatable flood barrier at Puri Grid Substation?"*), triggering instant $<10\text{ms}$ graph recalculation that restores downstream water treatment plants.
* **Vernacular Audio Dispatch:** Synthesizes localized Common Alerting Protocol (CAP) emergency voice alerts in **Odia**, **Hindi**, and **English** with a live animated audio equalizer.

---

## 4. Google Cloud Platform Native Foundation

* **Google Cloud Run:** Hosts the containerized Python 3.13 FastAPI backend containing Cython/NumPy physics solvers and NetworkX graph engines. Auto-scales from 0 to 50+ instances.
* **Google BigQuery GIS:** Manages hundreds of thousands of municipal infrastructure entities as native `GEOGRAPHY` objects, executing spatial queries (`ST_DWITHIN`, `ST_INTERSECTS`) in $<250\text{ms}$.
* **Vertex AI / Gemini 2.0 Flash:** Multimodal visual damage classification, counterfactual triage optimization, and vernacular broadcast generation.
* **Firebase App Hosting:** Next.js 14 frontend deployment with instant edge CDN distribution.

---

## 5. Repository Structure

```
aegis-cyclone-forecaster/
├── aegis_core/                 # Core deterministic computation engines
│   ├── physics.py              # Holland wind model & hydrodynamic surge bathymetry
│   ├── cascade_graph.py        # NetworkX multi-layer directed dependency solver
│   └── models.py               # Pydantic data schemas for infrastructure assets
├── services/                   # AI & cloud integrations
│   ├── vertex_agent.py         # Gemini 2.0 Flash ReAct tool-calling agent
│   ├── multimodal_vision.py    # Sentinel-2 satellite visual tile inspector
│   ├── heuristic_fallback.py   # Sub-5ms Dijkstra/Betweenness offline fail-safe
│   └── bigquery_service.py     # BigQuery GIS spatial query handler
├── api/                        # FastAPI REST application
│   └── main.py                 # Simulation, cascade, mitigation & dispatch endpoints
├── frontend/                   # Next.js 14 App Router WebGL interface
│   ├── src/components/
│   │   ├── ResilienceDeckMap.tsx           # Deck.gl 60 FPS WebGL map canvas
│   │   ├── ResilienceMetricsBar.tsx        # 48px HUD telemetry bar
│   │   ├── TimeScrubber.tsx                # Floating glass timeline scrubber pill
│   │   ├── IncidentDispatchConsole.tsx     # Vernacular voice alert drawer with equalizer
│   │   ├── MitigationDrawer.tsx            # Counterfactual mitigation laboratory
│   │   ├── SatelliteVisionInspector.tsx    # Multimodal Sentinel-2 tile analyzer
│   │   └── MapConfig.ts                    # Clean unmetered Esri basemap configuration
│   └── src/app/                            # App Router layouts and pages
├── data/                       # Spatial fixtures & satellite imagery
│   ├── seed_fani.py            # Generates Puri/Paradip infrastructure & surge GeoJSON
│   ├── seed_satellite_tiles.py # Generates Sentinel-2 multi-spectral crop tiles
│   └── tiles/                  # Satellite inspection crops
├── docs/                       # Hackathon submission documentation
│   ├── Aegis_Presentation_Track05.pdf     # Official presentation deck (<= 5MB)
│   ├── Aegis_Presentation_Track05.pptx    # Editable PowerPoint 16:9 presentation
│   ├── hackathon_submission.md            # Portal submission fields & metrics
│   ├── pitch_script_and_walkthrough.md    # 2.5-minute video recording script
│   └── cyclone_architecture_research.md   # Mathematical equations & literature review
├── Dockerfile                  # Production container spec for Google Cloud Run
├── cloudbuild.yaml             # Google Cloud Build CI/CD deployment pipeline
├── start_local.ps1             # One-click Windows development launcher
├── deploy_gcp.ps1              # One-click Google Cloud deployment script
└── requirements.txt            # Python dependencies
```

---

## 6. Quickstart (Run Locally in 60 Seconds)

### Option A: One-Click Launcher (Windows PowerShell)
```powershell
.\start_local.ps1
```

### Option B: Manual Setup

#### 1. Backend (FastAPI + Python)
```bash
# Setup virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # On Windows
# source .venv/bin/activate # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Seed GeoJSON datasets & Sentinel-2 tiles
python data/seed_fani.py
python data/seed_satellite_tiles.py

# Launch FastAPI backend
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```
Backend API interactive documentation will be live at: `http://127.0.0.1:8000/docs`

#### 2. Frontend (Next.js 14 WebGL Console)
```bash
cd frontend
npm install
npm run build
npm run start -p 3000
# or for hot-reloading dev mode:
# npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 7. Submission Artifacts

* **Public GitHub Repository:** [https://github.com/Styxoid/aegis-cyclone-forecaster](https://github.com/Styxoid/aegis-cyclone-forecaster)
* **Presentation Deck (PDF $\le$ 5MB):** [`docs/Aegis_Presentation_Track05.pdf`](docs/Aegis_Presentation_Track05.pdf)
* **Editable Slide Deck (PPTX):** [`docs/Aegis_Presentation_Track05.pptx`](docs/Aegis_Presentation_Track05.pptx)
* **2.5-Minute Pitch Script:** [`docs/pitch_script_and_walkthrough.md`](docs/pitch_script_and_walkthrough.md)
* **Submission Portal Checklist:** [`docs/hackathon_submission.md`](docs/hackathon_submission.md)

---

## 8. License

Developed by **Team GGR** for the **Google Cloud Build with AI: Code for Communities Hackathon (Second Edition)**. Released under the Apache 2.0 License.
