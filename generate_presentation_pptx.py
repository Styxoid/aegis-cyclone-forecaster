import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_aegis_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6] # completely blank layout

    # Color Palette
    BG_COLOR = RGBColor(11, 15, 25)         # Deep titanium navy
    CARD_BG = RGBColor(17, 24, 39)          # Card background
    CARD_BORDER = RGBColor(30, 41, 59)      # Border
    CYAN = RGBColor(6, 182, 212)            # Neon Cyan
    EMERALD = RGBColor(16, 185, 129)        # Emerald
    AMBER = RGBColor(245, 158, 11)          # Amber
    ROSE = RGBColor(239, 68, 68)            # Crimson / Rose
    WHITE = RGBColor(248, 250, 252)         # Primary Text
    MUTED = RGBColor(148, 163, 184)         # Secondary / Muted Text

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background() # no line

    def add_header(slide, badge_text, title_text, subtitle_text, slide_num):
        # Header Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.8), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(14, 34, 56)
        badge.line.color.rgb = CYAN
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = CYAN
        p_b.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10.0), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = WHITE

        # Subtitle
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(10.5), Inches(0.4))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = MUTED

        # Footer
        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.3))
        tf_foot = tb_foot.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = f"AEGIS  //  Track 05: Cyclone Resilience  |  Build with AI  |  Slide {slide_num} of 8"
        p_foot.font.size = Pt(9.5)
        p_foot.font.color.rgb = RGBColor(100, 116, 139)

    # ==========================================
    # SLIDE 1: HERO / TITLE
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1)

    # Sub-badge
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(5.8), Inches(0.38))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(14, 34, 56)
    b1.line.color.rgb = CYAN
    b1.line.width = Pt(1)
    tf_b1 = b1.text_frame
    p_b1 = tf_b1.paragraphs[0]
    p_b1.text = "GOOGLE CLOUD BUILD WITH AI: CODE FOR COMMUNITIES (2ND ED)"
    p_b1.font.size = Pt(10)
    p_b1.font.bold = True
    p_b1.font.color.rgb = CYAN
    p_b1.alignment = PP_ALIGN.CENTER

    # Main Brand Title
    tb_title = s1.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.0), Inches(1.4))
    tf_t = tb_title.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "AEGIS"
    p_t.font.size = Pt(64)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    # Tagline
    tb_tag = s1.shapes.add_textbox(Inches(1.0), Inches(3.1), Inches(11.2), Inches(1.1))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "Autonomous Physical-Topological Cyclone Impact & Infrastructure Vulnerability Forecaster bridging macro-meteorology and hyper-local civic resilience."
    p_tag.font.size = Pt(18)
    p_tag.font.color.rgb = RGBColor(203, 213, 225)

    # 4 Key Pillars Box
    pillars = [
        "Deterministic Holland Physics",
        "Topological NetworkX Graph",
        "Multimodal Gemini 2.0 Vision",
        "60 FPS WebGL Resilience Map"
    ]
    for i, pil in enumerate(pillars):
        left_pos = Inches(1.0 + (i * 2.85))
        pbox = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(4.5), Inches(2.7), Inches(0.7))
        pbox.fill.solid()
        pbox.fill.fore_color.rgb = CARD_BG
        pbox.line.color.rgb = CARD_BORDER
        pbox.line.width = Pt(1)
        tf_p = pbox.text_frame
        tf_p.word_wrap = True
        pp = tf_p.paragraphs[0]
        pp.text = f"◆ {pil}"
        pp.font.size = Pt(11)
        pp.font.bold = True
        pp.font.color.rgb = WHITE
        pp.alignment = PP_ALIGN.CENTER

    # Hero Meta
    tb_meta = s1.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.0), Inches(0.5))
    tf_meta = tb_meta.text_frame
    p_m = tf_meta.paragraphs[0]
    p_m.text = "Track: Track 05 — Cyclone Resilience  |  Team: Team GGR  |  Geography: Odisha Corridor (Puri & Paradip)\nStack: Google Cloud Run • Vertex AI / Gemini 2.0 Flash • BigQuery GIS • Next.js 14 WebGL"
    p_m.font.size = Pt(11)
    p_m.font.color.rgb = MUTED

    # ==========================================
    # SLIDE 2: THE PROBLEM (THE FATAL GAP)
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2)
    add_header(s2, "The Problem Statement", "The 'Fatal Gap' in Disaster Response", "Why traditional meteorological forecasts cause operational dispatch paralysis during Category 4+ cyclones", 2)

    col_data_s2 = [
        ("Failure 1: Coarse Grids vs. Asset Truth", ROSE, [
            "Numerical Weather Prediction models (IMD / GFS) output coarse 15–25 km grid cells.",
            "Cannot determine if a 132/33 kV substation with +1.1m plinth will be submerged by a 1.8m coastal storm surge.",
            "Result: Discoms keep transformers energized until explosive blowout, causing ₹15Cr+ damage and 6-week blackouts."
        ]),
        ("Failure 2: Isolated Maps vs. Cascades", AMBER, [
            "Portals show isolated flood polygons, ignoring directed dependency cascades:",
            "Substation Flooded ➔ Water Treatment Halts ➔ Hospital ICU Fuel Clock Starts (12h) ➔ Arterial Road Washed Out.",
            "Even if a hospital sits on high ground, diesel supply fails if road wading limit (>0.35m) is breached."
        ]),
        ("Failure 3: Single-Point IoT Blindness", CYAN, [
            "Coastal IoT weather sensors and edge anemometers are mechanically sheared at 180+ km/h winds.",
            "Sensor-reliant dashboards go dark at the exact moment of peak landfall crisis.",
            "Aegis Solution: Deterministic atmospheric physics simulate conditions without requiring surviving physical edge sensors."
        ])
    ]

    for i, (col_title, col_col, bullets) in enumerate(col_data_s2):
        left_pos = Inches(0.8 + (i * 3.95))
        cbox = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(3.8), Inches(4.8))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = col_col
        cbox.line.width = Pt(1)
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        
        p0 = tf_c.paragraphs[0]
        p0.text = col_title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = WHITE
        
        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = MUTED
            p_b.space_before = Pt(8)

    # ==========================================
    # SLIDE 3: SYSTEM ARCHITECTURE
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3)
    add_header(s3, "System Architecture", "The Hybrid Triple-Layer Resilience Engine", "Anchoring probabilistic AI reasoning to deterministic atmospheric physics and topological graph cascades", 3)

    col_data_s3 = [
        ("Layer 1: Deterministic Physics", CYAN, [
            "Holland (1980/2010) Parametric Radial Wind Field: calculates exact wind velocity profiles across radius r.",
            "Asymmetric Storm Translation: incorporates 22 km/h forward translation vector into right-front quadrant shear.",
            "Bathymetric Hydrodynamic Surge: computes inverse barometer effect (1cm/hPa) + onshore friction wind setup.",
            "Kaplan-DeMaria Inland Decay: models hourly kinetic energy dissipation over land."
        ]),
        ("Layer 2: Topological Graph Solver", EMERALD, [
            "NetworkX Multi-Layer Directed Dependency Graph G = (V, E).",
            "Dynamic Edge Severance: highway links severed when water depth exceeds 0.35m tanker wading threshold.",
            "Cut-Set Failure Propagation: electrical feeder severance halts water pump and starts hospital generator timers.",
            "Sub-50ms Graph Traversal: computes downstream isolation in real-time."
        ]),
        ("Layer 3: Cognitive Dispatch Agent", AMBER, [
            "Google Gemini 2.0 Flash Tool-Calling: ReAct agent orchestrating physics, graph solvers, and GIS queries.",
            "Multimodal Sentinel-2 Vision: analyzes mangrove canopy density and roof fragility.",
            "Vernacular Voice Synthesis: generates Common Alerting Protocol (CAP) broadcasts in Odia, Hindi, English.",
            "Sub-5ms Heuristic Fallback: zero-downtime offline fail-safe if network drops."
        ])
    ]

    for i, (col_title, col_col, bullets) in enumerate(col_data_s3):
        left_pos = Inches(0.8 + (i * 3.95))
        cbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(3.8), Inches(4.8))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = col_col
        cbox.line.width = Pt(1)
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        
        p0 = tf_c.paragraphs[0]
        p0.text = col_title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = WHITE
        
        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = MUTED
            p_b.space_before = Pt(8)

    # ==========================================
    # SLIDE 4: ZERO WRAPPER AI MOAT
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4)
    add_header(s4, "25% AI Rubric Depth", "The 'Zero-Wrapper' Technical Moat", "How Aegis avoids shallow LLM chatbot traps via multimodal satellite vision and deterministic tool-calling", 4)

    s4_boxes = [
        ("Multimodal Satellite Vision (Sentinel-2 Ingestion)", CYAN, [
            "Gemini 2.0 Flash directly ingests multi-spectral Sentinel-2 satellite crops of coastal estuaries.",
            "Mangrove Bio-Shield Density: Visually measures coastal forest degradation along Mahanadi/Devi estuaries, calculating natural wave dissipation factors.",
            "Informal Roof Material Index: Identifies vulnerable tin/thatch settlements within high-shear wind cones (>160 km/h) requiring immediate bus evacuations.",
            "Direct Physics Modulation: Automatically tunes empirical surface roughness length (z0) in Holland equations based on visual terrain classification."
        ]),
        ("Anti-Fragile Tool Calling & Offline Fail-Safe", AMBER, [
            "Gemini acts as an analytical orchestrator, not a text generation chatbot.",
            "ReAct Loop executes strict deterministic tools: query_infrastructure_cone(), simulate_hydro_wind_decay(), evaluate_graph_cascade(), dispatch_multilingual_cap().",
            "Sub-5ms Local Heuristic Engine: If Vertex AI undergoes internet dropouts, Aegis automatically shifts to an embedded Dijkstra/Betweenness Heuristic Engine. Operations continue with 0% downtime.",
            "Strict JSON Schema Enforcement: Guarantees hallucination-free spatial coordinates and verified dispatch payloads."
        ])
    ]

    for i, (box_title, box_col, bullets) in enumerate(s4_boxes):
        left_pos = Inches(0.8 + (i * 5.95))
        cbox = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(5.75), Inches(4.8))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = box_col
        cbox.line.width = Pt(1)
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        
        p0 = tf_c.paragraphs[0]
        p0.text = box_title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = WHITE
        
        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = MUTED
            p_b.space_before = Pt(10)

    # ==========================================
    # SLIDE 5: GCP NATIVE ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5)
    add_header(s5, "Cloud Infrastructure", "Google Cloud Native Architecture", "Serverless, horizontally scalable, sub-100ms spatial intelligence pipeline", 5)

    gcp_pillars = [
        ("Google Cloud Run", "Serverless Compute", CYAN, [
            "Stateless containerized Python FastAPI backend.",
            "Houses Holland physics models and NetworkX graph solver.",
            "Scales 0 to 50+ instances in seconds during active storm landfall events."
        ]),
        ("BigQuery GIS", "Spatial Database", EMERALD, [
            "Stores municipal infrastructure assets as native GEOGRAPHY objects.",
            "Executes sub-250ms spatial join queries (ST_DWITHIN, ST_INTERSECTS) against dynamic cyclone polygon cones."
        ]),
        ("Vertex AI / Gemini 2.0", "Cognitive Engine", AMBER, [
            "Multimodal satellite vision tile analysis and counterfactual triage planning.",
            "Synthesizes verified Common Alerting Protocol (CAP) civil protection broadcasts."
        ]),
        ("Next.js 14 + Deck.gl", "WebGL Console", ROSE, [
            "Hardware-accelerated 3D WebGL rendering running at locked 60 FPS.",
            "Overlays 3D extruded surge inundation depth and highway cut-sets on zero-token dark basemaps."
        ])
    ]

    for i, (g_title, g_sub, g_col, bullets) in enumerate(gcp_pillars):
        left_pos = Inches(0.8 + (i * 2.95))
        cbox = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(2.8), Inches(4.8))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = g_col
        cbox.line.width = Pt(1)
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        
        p0 = tf_c.paragraphs[0]
        p0.text = g_title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = WHITE

        p_sub = tf_c.add_paragraph()
        p_sub.text = g_sub.upper()
        p_sub.font.size = Pt(9)
        p_sub.font.bold = True
        p_sub.font.color.rgb = g_col
        
        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = MUTED
            p_b.space_before = Pt(8)

    # ==========================================
    # SLIDE 6: LIVE WORKING PROTOTYPE
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6)
    add_header(s6, "Live Working Prototype", "Tactical Command & Decision Console", "Production-grade, zero-lag interface built for Emergency Operations Centers (EOCs)", 6)

    proto_features = [
        ("Operational Decision Support", CYAN, [
            "4D Landfall Timeline Scrubber: Simulates Cyclone Fani landfall from T-00:00 to T-09:00 hours with smooth real-time interpolation of wind fields and surge envelopes.",
            "Dynamic Cascade Graph Layer: Visualizes electrical feeders (yellow), water pipelines (blue), and hospital logistics corridors (cyan) with dynamic failure pulsing.",
            "Telemetry Telemetry HUD: Real-time tracking of Max Wind (km/h), Peak Surge (m), Inundated Substations, Hospital Generator Countdown Clocks, and Severed Roads."
        ]),
        ("Tactical Mitigation Lab & Vernacular Radio", EMERALD, [
            "Counterfactual Mitigation Drawer: Emergency directors simulate interventions before dispatching crews ('What if we erect an inflatable flood barrier at Puri Grid Substation?' ➔ Graph recalculates in <10ms, restoring 3 downstream water pumps!).",
            "Multimodal Vision Inspector: Live modal analyzing Sentinel-2 multi-spectral satellite crops of Puri and Paradip.",
            "Vernacular Radio Broadcaster: Speech synthesis producing localized warnings in Odia, Hindi, and English with real-time audio waveform equalizer."
        ])
    ]

    for i, (p_title, p_col, bullets) in enumerate(proto_features):
        left_pos = Inches(0.8 + (i * 5.95))
        cbox = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(5.75), Inches(4.8))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = p_col
        cbox.line.width = Pt(1)
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        
        p0 = tf_c.paragraphs[0]
        p0.text = p_title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = WHITE
        
        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = MUTED
            p_b.space_before = Pt(10)

    # ==========================================
    # SLIDE 7: QUANTIFIABLE IMPACT
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7)
    add_header(s7, "Impact & Scalability", "Quantifiable Community & Economic Impact", "Saving critical infrastructure, municipal budgets, and human lives in vulnerable coastal districts", 7)

    # 4 Metric Cards across top
    metrics = [
        ("₹15+ Cr", "Per Substation Saved", CYAN),
        ("450+", "ICU Beds Preserved", EMERALD),
        ("3", "Vernacular Dialects (Odia/Hin/Eng)", AMBER),
        ("< 50ms", "Cascade Compute Latency", ROSE)
    ]
    for i, (m_val, m_lbl, m_col) in enumerate(metrics):
        left_pos = Inches(0.8 + (i * 2.95))
        mbox = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(2.8), Inches(1.2))
        mbox.fill.solid()
        mbox.fill.fore_color.rgb = CARD_BG
        mbox.line.color.rgb = CARD_BORDER
        mbox.line.width = Pt(1)
        tf_m = mbox.text_frame
        tf_m.word_wrap = True
        
        p_val = tf_m.paragraphs[0]
        p_val.text = m_val
        p_val.font.size = Pt(24)
        p_val.font.bold = True
        p_val.font.color.rgb = m_col
        
        p_lbl = tf_m.add_paragraph()
        p_lbl.text = m_lbl.upper()
        p_lbl.font.size = Pt(8.5)
        p_lbl.font.color.rgb = MUTED

    # 2 Impact deep dive boxes below
    s7_impacts = [
        ("Infrastructure Resilience (Transformer Protection)", EMERALD, [
            "By providing a 3-hour verified lead time prior to surge inundation, discoms safely de-energize transformers and isolate transformer bushings before saltwater contact.",
            "Eliminates explosive short-circuits and prevents 4 to 6 weeks of post-cyclone grid blackouts.",
            "Saves an estimated ₹12–18 Crore ($1.5M–$2.2M) per substation in replacement hardware."
        ]),
        ("Healthcare & Civic Defense (Zero ICU Blackouts)", CYAN, [
            "Automated identification of road cut-offs allows district collectors to preposition high-axle diesel tankers at hospitals or reroute supply convoys via high-elevation inland bypasses.",
            "Prevents generator fuel exhaustion for over 450 critical ICU and neonatal patients.",
            "Streams localized Common Alerting Protocol (CAP) audio alerts directly in Odia and Hindi to coastal panchayats."
        ])
    ]

    for i, (i_title, i_col, bullets) in enumerate(s7_impacts):
        left_pos = Inches(0.8 + (i * 5.95))
        cbox = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(3.3), Inches(5.75), Inches(3.4))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = i_col
        cbox.line.width = Pt(1)
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        
        p0 = tf_c.paragraphs[0]
        p0.text = i_title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = WHITE
        
        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(10.5)
            p_b.font.color.rgb = MUTED
            p_b.space_before = Pt(8)

    # ==========================================
    # SLIDE 8: ROADMAP & TEAM
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8)
    add_header(s8, "Roadmap & Readiness", "Production Roadmap & Team GGR", "Path to national deployment with state disaster management authorities", 8)

    s8_boxes = [
        ("Production Roadmap", CYAN, [
            "Phase 1 (Complete): High-fidelity Holland physics, NetworkX dependency cascade, Gemini 2.0 Flash tool-calling, 60 FPS WebGL console, multimodal satellite vision, and vernacular radio synthesizer.",
            "Phase 2 (Q3 2026): Live integration with IMD NWF API streaming feeds, automated drone photogrammetry ingestion, and offline edge deployment for mobile command vans.",
            "Phase 3 (Q4 2026): Pan-India coastal expansion across Andhra Pradesh, Tamil Nadu, West Bengal, and Gujarat coastline networks."
        ]),
        ("Why Aegis Wins Track 05", AMBER, [
            "1. Not a Toy Chatbot: Anchors AI reasoning directly to verified peer-reviewed hydrodynamic and atmospheric physics equations.",
            "2. Solves the Real Problem: Addresses the fatal gap between macro weather predictions and cross-sector infrastructure failure cascades.",
            "3. Production Engineering: Complete, zero-lag, self-contained prototype deploying on Google Cloud Run with sub-100ms latency.",
            "Engineered with dedication by Team GGR for Google Cloud Build with AI."
        ])
    ]

    for i, (box_title, box_col, bullets) in enumerate(s8_boxes):
        left_pos = Inches(0.8 + (i * 5.95))
        cbox = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.9), Inches(5.75), Inches(4.8))
        cbox.fill.solid()
        cbox.fill.fore_color.rgb = CARD_BG
        cbox.line.color.rgb = box_col
        cbox.line.width = Pt(1)
        tf_c = cbox.text_frame
        tf_c.word_wrap = True
        
        p0 = tf_c.paragraphs[0]
        p0.text = box_title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = WHITE
        
        for b in bullets:
            p_b = tf_c.add_paragraph()
            p_b.text = f"• {b}"
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = MUTED
            p_b.space_before = Pt(10)

    # Save PPTX
    out_path = os.path.abspath("docs/Aegis_Presentation_Track05.pptx")
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")
    print(f"File size: {os.path.getsize(out_path)} bytes")

if __name__ == "__main__":
    create_aegis_pptx()
