# AegisSurge: Official 2.5-Minute Video Pitch Script & Demo Walkthrough Cue Sheet
**Google Cloud Build with AI: Code for Communities (Second Edition)**  
**Track 05:** Track-Based Cyclone Impact & Infrastructure Vulnerability Forecaster  
**Target Video Duration:** 2 minutes 30 seconds (150 seconds)  
**Presenters:** Team GGR  

---

## Video Production Cue Sheet & Time-Coded Choreography

| Timestamp | Visual Screen Action (What to Record) | Voiceover Script (What to Say) | Audio / SFX |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:20** | **Map View:** Fullscreen dark-mode WebGL map of Odisha coast. Camera centered over Bay of Bengal as Cyclone Fani approaches. | *"When a Category 4 or 5 cyclone approaches the Indian coast, disaster management officers don't suffer from a lack of wind speed charts. They suffer from operational dispatch paralysis caused by unmodeled infrastructure dependencies."* | Low, ambient radar sweep tone. |
| **0:20 - 0:40** | **Zoom into Puri:** Show 3D extruded cyan storm-surge polygons pushing onto the coast. The Holland wind radius circle is visible. | *"Existing weather alerts tell us winds will reach 200 km/h across entire districts. But they can't tell a municipal collector if the 132kV Puri grid substation will flood, or if the arterial highway feeding hospital generators will be washed out by a 3.5-meter storm surge."* | Subtle wind ambient audio. |
| **0:40 - 1:05** | **The 60-Second "Wow" Moment:** Drag timeline scrubber from $T-6\text{h} \to T=0\text{h}$ (Landfall). Watch the Puri 132kV Substation turn RED (`FAILED`). Dependency arcs to Puri District Hospital snap from glowing cyan to crimson. Hospital status flips to amber: `RUNNING ON GENERATOR: 12h FUEL`. Simultaneously, Highway NH-316 turns red (`SEVERED`). | *"Here is AegisSurge in action. We couple deterministic physics—the Holland wind field decay model and hydrodynamic surge bathymetry—with a NetworkX topological graph cascade engine. As Fani makes landfall at T=0, our physical model submerges the coastal substation. Instantly, our graph solver propagates the cascading collapse: Puri District Hospital loses grid power, begins a 12-hour fuel countdown, and its primary highway supply corridor is severed by flood waters."* | Crisp click sound as arcs snap red. |
| **1:05 - 1:25** | **Autonomous Incident Command & Audio:** Expand the right Incident Dispatch Drawer. Click **"Broadcast Audio"** on the Odia language radio bulletin. The visualizer pulses with audio. | *"AegisSurge avoids the shallow LLM wrapper trap. Gemini 2.0 Flash acts as an analytical cognitive dispatcher. It detects the network cut-set, calculates high-axle inland rerouting, and synthesizes localized Common Alerting Protocol broadcasts in Odia, Hindi, and English over VHF Marine and emergency radio frequencies."* | AI voice speaks in Odia: *"ଜରୁରୀ ସୂଚନା: ଗ୍ରୀଡ୍ ସବ୍‌ଷ୍ଟେସନରେ ବିଦ୍ୟୁତ ସରବରାହ ବନ୍ଦ ହୋଇଛି..."* |
| **1:25 - 1:45** | **Satellite Vision Inspector:** Click **"Satellite Vision"** in top bar. Inspect the Paradip Port 132kV Substation Sentinel-2 tile. Run inference to show Mangrove bio-shield density (15%), Drainage choke risk (88%), and Injected damage factor (1.82). | *"To evaluate hyper-local vulnerability, AegisSurge integrates multi-spectral Sentinel-2 satellite crops. Gemini 2.0 Flash visually parses mangrove bio-shield degradation, perimeter trench siltation, and roof material fragility, injecting calibrated empirical multipliers directly into our physical damage equations."* | UI modal transition sound. |
| **1:45 - 2:10** | **The Counterfactual Mitigation Lab:** Open Mitigation Lab. Toggle on: *"Erect Demountable Surge Barriers at Paradip 132kV Substation"*. Watch the network instantly recalculate: Paradip substation turns back to green; 3 critical downstream assets and water intakes are saved! | *"Crucially, AegisSurge is counterfactual. In our Mitigation Lab, commanders can test interventions hours before landfall. By deploying demountable flood barriers at Paradip, our solver proves we prevent dielectric switchgear explosion, keeping water treatment and port trauma facilities operational throughout the storm."* | Success chime as metrics update from 6 failed to 3 failed. |
| **2:10 - 2:30** | **Google Cloud Architecture Slide / Codebase:** Quick cut to Google Cloud Run console, BigQuery GIS SQL schema (`ST_DWITHIN`, `ST_INTERSECTS`), and GitHub repo structure. | *"Architected natively for Google Cloud, AegisSurge leverages containerized FastAPI on Cloud Run, S2-indexed spatial queries on BigQuery GIS, and Gemini 2.0 Flash on Vertex AI—backed by a sub-5ms deterministic heuristic fail-safe that guarantees zero downtime in disconnected crisis environments."* | Professional upbeat tech swell. |
| **2:30 - 2:45** | **Conclusion & Call to Action:** Return to full map view with live telemetry HUD. Display Team GGR and GDG India Hackathon branding. | *"AegisSurge transforms passive disaster monitoring into proactive, asset-level resilience. Built for coastal communities. Built with Google Cloud. Thank you."* | Outro music fade. |

---

## Recording Checklist & Best Practices

1. **Resolution & Scaling:**
   * Record screen at **1920x1080 (1080p, 60 FPS)** using OBS Studio or Chrome Screen Recorder.
   * Set browser zoom to **100%** to preserve crisp typography and 1px borders.
2. **Audio Setup:**
   * Use an external condenser or headset microphone.
   * Ensure system audio recording is enabled so the browser's Odia/Hindi voice broadcast is clearly audible.
3. **Pacing:**
   * Practice the slider drag at $0:45$ so the visual cascade coincides precisely with the word *"propagation"*.
   * Keep mouse movements smooth and intentional.
