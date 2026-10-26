"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1 | Platform ID: 6ac4c98d1dcde6d7857c1642
Author: Expert Full-Stack AI Engineer

An intelligent decision-support system analyzing site photos to audit PPE safety compliance,
classify concrete cracks with severity scores, estimate construction costs and real estate
valuation in INR, and provide weather-aware daily engineering protocols.
"""

import os
import json
import io
import time
from datetime import datetime
from PIL import Image
import streamlit as st

# Local modules
from config import (
    APP_TITLE, APP_SUBTITLE, VERSION,
    LOCATION_TIERS, STRUCTURE_TYPES, WEATHER_CONDITIONS,
    PRESET_ENGINEERING_PROMPTS, DEFAULT_VISION_MODEL
)
from modules.gemini_client import GeminiConstructionClient
from modules.safety_audit import run_safety_audit
from modules.crack_diagnostics import run_crack_diagnostics
from modules.planning_valuation import calculate_project_metrics, generate_pollinations_render_url
from modules.weather_advisory import get_weather_protocols, ask_assistant


# ------------------------------------------------------------------------------
# 1. Page Configuration & Styling
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{APP_TITLE} | Skill Wallet",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load External CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ------------------------------------------------------------------------------
# 2. Session State Initialization
# ------------------------------------------------------------------------------
if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = os.getenv("GEMINI_API_KEY", "")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {
            "role": "assistant",
            "content": "👋 Greetings Engineer. I am your **Senior Civil & Structural Site Assistant**. Ask me any technical query grounded in **IS 456:2000**, **OSHA 29 CFR 1926**, **IS 875**, or site curing & safety protocols."
        }
    ]

if "safety_result" not in st.session_state:
    st.session_state["safety_result"] = None

if "crack_result" not in st.session_state:
    st.session_state["crack_result"] = None

if "render_seed" not in st.session_state:
    st.session_state["render_seed"] = 101


# ------------------------------------------------------------------------------
# 3. Sidebar: Security, API Key, Model & Architecture Overview
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
        <span style="font-size:32px;">🏗️</span>
        <div>
            <div style="font-weight:800; font-size:16px; color:#f8fafc; letter-spacing:-0.02em;">CONSTRUCTION AI</div>
            <div style="font-size:11px; color:#38bdf8; font-weight:600;">CAPSTONE PROJECT 1</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔑 Authentication & Mode")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=st.session_state["gemini_api_key"],
        type="password",
        placeholder="AIzaSy... (Leave blank for Demo Mode)",
        help="Supply your Google Gemini API key for live multimodal analysis. If left blank, system operates in high-fidelity Demonstration Fallback mode."
    )

    if api_key_input != st.session_state["gemini_api_key"]:
        st.session_state["gemini_api_key"] = api_key_input.strip()
        st.rerun()

    # Initialize Gemini Client
    client = GeminiConstructionClient(api_key=st.session_state["gemini_api_key"])

    if client.is_demo_mode():
        st.markdown("""
        <div style="background:rgba(168, 85, 247, 0.12); border:1px solid rgba(168, 85, 247, 0.35); border-radius:8px; padding:10px; margin-bottom:14px;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#c084fc;"></span>
                <strong style="color:#e9d5ff; font-size:12px;">DEMONSTRATION MODE</strong>
            </div>
            <div style="font-size:11px; color:#cbd5e1; margin-top:4px;">
                Running on built-in IS 456 & OSHA heuristic benchmarks. Zero external API calls required.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(16, 185, 129, 0.12); border:1px solid rgba(16, 185, 129, 0.35); border-radius:8px; padding:10px; margin-bottom:14px;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#34d399;"></span>
                <strong style="color:#a7f3d0; font-size:12px;">LIVE GEMINI 1.5 CONNECTED</strong>
            </div>
            <div style="font-size:11px; color:#cbd5e1; margin-top:4px;">
                Multimodal vision & chat enabled via Google Gemini API.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Architecture Overview
    st.markdown("### 🏛️ Engineering Standards")
    st.markdown("""
    - **OSHA 29 CFR 1926**: Construction Safety
    - **IS 456:2000**: Plain & Reinforced Concrete
    - **IS 875 (Part 3)**: Design Wind Loads
    - **IS 13416**: Safety Precautions in Construction
    - **IS 7861**: Hot/Cold Weather Concreting
    - **CPWD & RERA**: Valuation Benchmarks
    """)

    st.markdown("---")
    st.markdown("### 📋 Platform Info")
    st.markdown(f"""
    - **Platform ID**: `6ac4c98d1dcde6d7857c1642`
    - **Category**: Generative AI | Real Estate Decision Support
    - **Deployment**: Streamlit Community Cloud
    - **Version**: `{VERSION}`
    """)


# ------------------------------------------------------------------------------
# 4. Hero Banner
# ------------------------------------------------------------------------------
st.markdown(f"""
<div class="construction-hero-banner">
    <div class="hero-title">
        <span>🏗️</span> {APP_TITLE}
    </div>
    <p class="hero-subtitle">
        {APP_SUBTITLE}
    </p>
    <div style="margin-top: 14px; display: flex; flex-wrap: wrap; gap: 8px;">
        <span class="badge-tag osha">🛡️ OSHA 1926 Verified</span>
        <span class="badge-tag is456">📐 IS 456:2000 Standard</span>
        <span class="badge-tag {'live' if not client.is_demo_mode() else 'demo'}">
            {'🟢 Gemini 1.5 Multimodal' if not client.is_demo_mode() else '🟣 Demonstration Mode'}
        </span>
        <span class="badge-tag is456">⚡ 100% Zero-DB Serverless</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 5. Main Navigation Tabs
# ------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit",
    "🔍 Crack Diagnostics & Structural Integrity",
    "📊 Planning & Real Estate Valuation",
    "🌤️ Weather Advisory & Site Assistant"
])


# ==============================================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# ==============================================================================
with tab1:
    st.markdown("### 🦺 Construction Site Safety & PPE Compliance Audit")
    st.markdown("Upload a site photograph to perform an AI visual audit of worker Personal Protective Equipment (helmets, high-vis vests, steel-toe boots, safety harnesses) under OSHA 29 CFR 1926 and IS standards.")

    col1, col2 = st.columns([1, 1], gap="medium")

    sample_safety_path = os.path.join(os.path.dirname(__file__), "assets", "sample_site_safety.jpg")

    with col1:
        st.markdown("#### 1. Input Inspection Image")
        uploaded_safety_img = st.file_uploader(
            "Upload Construction Site Photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="safety_uploader"
        )

        use_sample_safety = st.button("📸 Load Built-in High-Risk Inspection Sample", key="load_sample_safety")

        image_to_analyze = None
        if uploaded_safety_img is not None:
            image_to_analyze = Image.open(uploaded_safety_img)
            st.image(image_to_analyze, caption="Uploaded Site Photo", use_container_width=True)
        elif use_sample_safety or (st.session_state["safety_result"] is not None and not uploaded_safety_img):
            if os.path.exists(sample_safety_path):
                image_to_analyze = Image.open(sample_safety_path)
                st.image(image_to_analyze, caption="Sample Site Inspection Image (Reinforced Concrete Deck)", use_container_width=True)

        audit_btn = st.button("🚀 Run AI Safety & PPE Audit", type="primary", use_container_width=True, disabled=(image_to_analyze is None))

        if audit_btn and image_to_analyze is not None:
            with st.spinner("Analyzing site hazards and PPE compliance against OSHA & IS 456..."):
                st.session_state["safety_result"] = run_safety_audit(image_to_analyze, client)

    with col2:
        st.markdown("#### 2. Audit Findings & Metrics")
        res = st.session_state["safety_result"]

        if res:
            # Source Tag
            src = res.get("_source", "Engine")
            is_live = res.get("_is_live", False)
            st.markdown(f"""
            <div style="font-size:12px; margin-bottom:12px; color:{'#34d399' if is_live else '#c084fc'}; font-weight:600;">
                ℹ️ Audit Engine: {src}
            </div>
            """, unsafe_allow_html=True)

            # Top KPI Metric Cards
            score = res.get("safety_score", 0)
            status = res.get("overall_status", "Audited")
            workers_count = res.get("workers_detected_count", 0)
            hazards = res.get("identified_site_hazards", [])

            # Status pill color class
            status_class = "compliant" if score >= 80 else ("warning" if score >= 50 else "critical")

            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"""
                <div class="metric-card-custom">
                    <div class="card-label">Safety Score</div>
                    <div class="card-value" style="color:{'#10b981' if score>=80 else ('#f59e0b' if score>=50 else '#ef4444')};">{score}/100</div>
                    <div class="card-footer">OSHA Composite Index</div>
                </div>
                """, unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"""
                <div class="metric-card-custom">
                    <div class="card-label">Overall Status</div>
                    <div style="margin-top:6px;"><span class="status-pill {status_class}">{status}</span></div>
                    <div class="card-footer">Site Regulatory State</div>
                </div>
                """, unsafe_allow_html=True)
            with m_col3:
                st.markdown(f"""
                <div class="metric-card-custom">
                    <div class="card-label">Workers Detected</div>
                    <div class="card-value">{workers_count}</div>
                    <div class="card-footer">{len(hazards)} Active Hazards</div>
                </div>
                """, unsafe_allow_html=True)

            # Summary Callout
            st.markdown(f"""
            <div style="background:rgba(30, 41, 59, 0.6); border-left:4px solid #3b82f6; padding:12px 16px; border-radius:6px; margin:16px 0;">
                <strong style="color:#93c5fd; font-size:13px;">Executive Safety Brief:</strong>
                <p style="margin:4px 0 0 0; font-size:13px; color:#cbd5e1;">{res.get('summary', 'Audit complete.')}</p>
            </div>
            """, unsafe_allow_html=True)

            # PPE Detection Checklist
            st.markdown("##### 🛡️ Worker PPE Detection Checklist")
            ppe_items = res.get("ppe_detection", [])
            for ppe in ppe_items:
                p_status = ppe.get("status", "Unknown")
                p_class = "compliant" if "Compliant" in p_status and "Non" not in p_status else ("warning" if "Partial" in p_status else "critical")
                det = ppe.get("detected_count", 0)
                tot = ppe.get("total_workers", 0)
                std = ppe.get("governing_standard", "")
                obs = ppe.get("observations", "")

                st.markdown(f"""
                <div style="background:rgba(15, 23, 42, 0.4); border:1px solid rgba(148, 163, 184, 0.1); border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#f1f5f9; font-size:13px;">{ppe.get('item', 'PPE Item')}</span>
                        <span class="status-pill {p_class}">{p_status} ({det}/{tot})</span>
                    </div>
                    <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Standard: <code>{std}</code></div>
                    <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">{obs}</div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("👈 Upload an image or click 'Load Built-in High-Risk Inspection Sample' and click 'Run AI Safety & PPE Audit' to inspect safety compliance.")

    # Identified Site Hazards Section (Full Width)
    if res and res.get("identified_site_hazards"):
        st.markdown("---")
        st.markdown("#### 🚨 Identified Site Hazards & Engineering Remedies")
        haz_cols = st.columns(len(res["identified_site_hazards"]))
        for idx, haz in enumerate(res["identified_site_hazards"]):
            sev = haz.get("severity", "Medium")
            sev_class = "critical" if sev == "Critical" else ("warning" if sev == "High" else "medium")
            with haz_cols[idx % len(haz_cols)]:
                st.markdown(f"""
                <div class="hazard-box {sev_class}">
                    <div class="hazard-title">
                        <span>{haz.get('hazard_id', 'HAZ')}: {haz.get('title', 'Hazard')}</span>
                        <span class="status-pill {sev_class}">{sev}</span>
                    </div>
                    <div style="font-size:12px; color:#94a3b8; margin:4px 0;">
                        <strong>Zone:</strong> {haz.get('location_zone', 'N/A')}<br/>
                        <strong>OSHA Violation:</strong> <code>{haz.get('osha_violation', 'N/A')}</code><br/>
                        <strong>IS Code:</strong> <code>{haz.get('is_standard', 'N/A')}</code>
                    </div>
                    <div class="hazard-remedy">
                        <strong style="color:#f59e0b;">Engineering Remedy:</strong><br/>
                        {haz.get('corrective_remedy', 'Remediation advised.')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Immediate Actions Checklist & Download Report
        st.markdown("#### 📝 Immediate Remedial Action Protocol")
        actions = res.get("immediate_remedial_actions", [])
        for act in actions:
            st.checkbox(act, value=False, key=f"remedy_{act[:20]}")

        # JSON Download Button
        json_str = json.dumps(res, indent=2)
        st.download_button(
            label="📥 Download Structured JSON Safety Report",
            data=json_str,
            file_name=f"site_safety_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


# ==============================================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# ==============================================================================
with tab2:
    st.markdown("### 🔍 Concrete Crack Diagnostics & Structural Integrity")
    st.markdown("Classify concrete/wall defect mechanism (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling) with crack width gauge (mm), root cause analysis, and prescribed engineering repairs under IS 456:2000.")

    c_col1, c_col2 = st.columns([1, 1], gap="medium")
    sample_crack_path = os.path.join(os.path.dirname(__file__), "assets", "sample_concrete_crack.jpg")

    with c_col1:
        st.markdown("#### 1. Input Concrete Surface Image")
        uploaded_crack_img = st.file_uploader(
            "Upload Concrete / Masonry Photo (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader"
        )

        use_sample_crack = st.button("📸 Load Built-in Shear Crack Sample", key="load_sample_crack")

        crack_img_to_analyze = None
        if uploaded_crack_img is not None:
            crack_img_to_analyze = Image.open(uploaded_crack_img)
            st.image(crack_img_to_analyze, caption="Uploaded Concrete Defect Photo", use_container_width=True)
        elif use_sample_crack or (st.session_state["crack_result"] is not None and not uploaded_crack_img):
            if os.path.exists(sample_crack_path):
                crack_img_to_analyze = Image.open(sample_crack_path)
                st.image(crack_img_to_analyze, caption="Sample Defect Image (RCC Column Diagonal Shear Crack)", use_container_width=True)

        diag_btn = st.button("🔬 Run Structural Crack Diagnostics", type="primary", use_container_width=True, disabled=(crack_img_to_analyze is None))

        if diag_btn and crack_img_to_analyze is not None:
            with st.spinner("Analyzing concrete fissure geometry and stress kinematics..."):
                st.session_state["crack_result"] = run_crack_diagnostics(crack_img_to_analyze, client)

    with c_col2:
        st.markdown("#### 2. Diagnostic Assessment")
        c_res = st.session_state["crack_result"]

        if c_res:
            c_src = c_res.get("_source", "Engine")
            c_is_live = c_res.get("_is_live", False)
            st.markdown(f"""
            <div style="font-size:12px; margin-bottom:12px; color:{'#34d399' if c_is_live else '#c084fc'}; font-weight:600;">
                ℹ️ Diagnostics Engine: {c_src}
            </div>
            """, unsafe_allow_html=True)

            defect_type = c_res.get("defect_type", "Structural Crack")
            width_mm = c_res.get("estimated_crack_width_mm", 0.0)
            urgency = c_res.get("urgency", "Moderate")
            health_score = c_res.get("structural_integrity_score", 70)
            element = c_res.get("affected_element", "RCC Member")

            urg_class = "critical" if "Immediate" in urgency or "High" in urgency else ("warning" if "Moderate" in urgency else "compliant")

            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.markdown(f"""
                <div class="metric-card-custom">
                    <div class="card-label">Defect Type</div>
                    <div style="font-size:16px; font-weight:700; color:#38bdf8; margin:6px 0;">{defect_type}</div>
                    <div class="card-footer">{element}</div>
                </div>
                """, unsafe_allow_html=True)
            with kpi2:
                st.markdown(f"""
                <div class="metric-card-custom">
                    <div class="card-label">Crack Width (mm)</div>
                    <div class="card-value" style="color:{'#ef4444' if width_mm > 0.3 else '#f59e0b'};">{width_mm:.2f} mm</div>
                    <div class="card-footer">IS 456 Permissible: 0.20mm</div>
                </div>
                """, unsafe_allow_html=True)
            with kpi3:
                st.markdown(f"""
                <div class="metric-card-custom">
                    <div class="card-label">Urgency Level</div>
                    <div style="margin-top:6px;"><span class="status-pill {urg_class}">{urgency}</span></div>
                    <div class="card-footer">Structural Health: {health_score}/100</div>
                </div>
                """, unsafe_allow_html=True)

            # Mechanism Callout
            st.markdown(f"""
            <div style="background:rgba(30, 41, 59, 0.6); border-left:4px solid #f59e0b; padding:12px 16px; border-radius:6px; margin:16px 0;">
                <strong style="color:#fbbf24; font-size:13px;">Failure Mechanism:</strong>
                <p style="margin:4px 0 0 0; font-size:13px; color:#cbd5e1;">{c_res.get('primary_failure_mechanism', 'Under analysis.')}</p>
            </div>
            """, unsafe_allow_html=True)

            # Standard Compliance
            std_info = c_res.get("governing_standard_compliance", {})
            st.markdown(f"""
            <div style="background:rgba(15, 23, 42, 0.5); border:1px solid rgba(148, 163, 184, 0.15); border-radius:8px; padding:12px; margin-bottom:12px;">
                <div style="font-weight:700; color:#f1f5f9; font-size:13px;">⚖️ Governing Standard: {std_info.get('is_code', 'IS 456:2000')}</div>
                <div style="font-size:12px; color:#f87171; margin-top:4px;"><strong>Status:</strong> {std_info.get('compliance_status', 'Limit exceeded')}</div>
            </div>
            """, unsafe_allow_html=True)

            # Root Causes List
            st.markdown("##### 🔍 Identified Root Causes")
            for rc in c_res.get("root_causes", []):
                st.markdown(f"- ⚠️ {rc}")

        else:
            st.info("👈 Upload a concrete crack image or click 'Load Built-in Shear Crack Sample' to begin diagnostics.")

    # Recommended Engineering Repairs (Full Width)
    if c_res and c_res.get("recommended_engineering_repairs"):
        st.markdown("---")
        st.markdown("#### 🛠️ Recommended Structural Engineering Repair Protocol")
        repairs = c_res.get("recommended_engineering_repairs", [])
        r_cols = st.columns(len(repairs))
        for i, rep in enumerate(repairs):
            with r_cols[i % len(r_cols)]:
                st.markdown(f"""
                <div style="background:rgba(15, 23, 42, 0.6); border:1px solid rgba(59, 130, 246, 0.25); border-radius:10px; padding:16px; height:100%;">
                    <div style="font-size:11px; font-weight:800; color:#60a5fa; text-transform:uppercase; letter-spacing:0.05em;">Step {rep.get('step', i+1)}</div>
                    <div style="font-weight:700; color:#f8fafc; font-size:14px; margin:6px 0;">{rep.get('method', 'Repair Method')}</div>
                    <div style="font-size:12px; color:#cbd5e1; margin-bottom:8px;">{rep.get('specification', '')}</div>
                    <div style="font-size:11px; color:#fbbf24; border-top:1px dashed rgba(148, 163, 184, 0.2); padding-top:6px;">
                        <strong>Spec:</strong> {rep.get('material_grade', 'Engineering Grade')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if c_res.get("monitoring_advisory"):
            st.markdown(f"""
            <div style="background:rgba(20, 83, 45, 0.2); border:1px solid rgba(16, 185, 129, 0.3); border-radius:8px; padding:12px 16px; margin-top:16px;">
                <strong style="color:#34d399; font-size:13px;">📡 Structural Health Monitoring Advisory:</strong>
                <p style="margin:4px 0 0 0; font-size:13px; color:#a7f3d0;">{c_res.get('monitoring_advisory')}</p>
            </div>
            """, unsafe_allow_html=True)

        # JSON Download Button
        crack_json = json.dumps(c_res, indent=2)
        st.download_button(
            label="📥 Download Forensic Structural Report (JSON)",
            data=crack_json,
            file_name=f"crack_diagnostics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


# ==============================================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# ==============================================================================
with tab3:
    st.markdown("### 📊 Construction Planning, Material BOQ & Real Estate Valuation")
    st.markdown("Estimate total project budget, CapEx incurred, current asset valuation in INR (Lakhs/Crores), and steel/cement requirement metrics with conceptual 3D architectural rendering integration.")

    p_col1, p_col2 = st.columns([1, 1], gap="medium")

    with p_col1:
        st.markdown("#### 1. Project Specifications")
        selected_structure = st.selectbox(
            "Structure Type & Architectural System",
            options=list(STRUCTURE_TYPES.keys()),
            index=0
        )

        b_sqft = st.number_input(
            "Total Built-up Area (Sq.Ft.)",
            min_value=500,
            max_value=2000000,
            value=25000,
            step=2500,
            help="Total gross constructed floor area in square feet."
        )

        selected_tier = st.selectbox(
            "Location Tier (Indian Real Estate Market)",
            options=list(LOCATION_TIERS.keys()),
            index=0
        )

        comp_pct = st.slider(
            "Construction Completion Progress (%)",
            min_value=0.0,
            max_value=100.0,
            value=45.0,
            step=1.0,
            help="Milestone completion percentage of the project."
        )

    # Calculate Metrics
    metrics = calculate_project_metrics(
        structure_type=selected_structure,
        built_up_sqft=b_sqft,
        location_tier=selected_tier,
        completion_percentage=comp_pct
    )

    with p_col2:
        st.markdown("#### 2. Capital & Valuation Summary (INR)")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.markdown(f"""
            <div class="metric-card-custom">
                <div class="card-label">Total Project Budget</div>
                <div class="card-value" style="color:#60a5fa;">{metrics['total_budget_formatted']}</div>
                <div class="card-footer">Rate: ₹{metrics['construction_rate_per_sqft']:,} / sq.ft.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card-custom" style="margin-top:12px;">
                <div class="card-label">CapEx Incurred</div>
                <div class="card-value" style="color:#f59e0b;">{metrics['capex_incurred_formatted']}</div>
                <div class="card-footer">Remaining: {metrics['capex_remaining_formatted']}</div>
            </div>
            """, unsafe_allow_html=True)
        with v_col2:
            st.markdown(f"""
            <div class="metric-card-custom">
                <div class="card-label">Current Asset Valuation</div>
                <div class="card-value" style="color:#34d399;">{metrics['current_valuation_formatted']}</div>
                <div class="card-footer">At {comp_pct:.0f}% Completion Stage</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card-custom" style="margin-top:12px;">
                <div class="card-label">Valuation on Completion</div>
                <div class="card-value" style="color:#a78bfa;">{metrics['completed_valuation_formatted']}</div>
                <div class="card-footer">Projected Finished Market Value</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Milestone Progress Bar
    st.markdown("#### 🏗️ Construction Milestone Progress Bar")
    st.progress(comp_pct / 100.0)

    # Milestone Cards
    ms_cols = st.columns(5)
    for idx, ms in enumerate(metrics["milestones"]):
        m_status = ms["status"]
        m_color = "#34d399" if m_status == "Completed" else ("#fbbf24" if m_status == "In Progress" else "#64748b")
        with ms_cols[idx]:
            st.markdown(f"""
            <div style="background:rgba(15, 23, 42, 0.5); border-top:3px solid {m_color}; border-radius:6px; padding:10px; text-align:center;">
                <div style="font-size:11px; font-weight:700; color:{m_color}; text-transform:uppercase;">{m_status}</div>
                <div style="font-size:12px; font-weight:600; color:#f8fafc; margin-top:4px;">{ms['name']}</div>
                <div style="font-size:11px; color:#94a3b8; margin-top:2px;">Weight: {ms['weight']}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Materials Quantity Surveying (BOQ)
    st.markdown("#### 🧱 Bill of Quantities (BOQ) & Material Metrics")
    mats = metrics["materials"]
    boq_col1, boq_col2, boq_col3 = st.columns(3)

    with boq_col1:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="card-label">Cement Bags (50kg OPC/PPC)</div>
            <div class="card-value" style="font-size:24px;">{mats['cement_bags_total']:,} Bags</div>
            <div style="margin-top:8px; font-size:12px; color:#94a3b8;">
                Consumed: <strong style="color:#f59e0b;">{mats['cement_consumed']:,}</strong> | Remaining: <strong style="color:#34d399;">{mats['cement_remaining']:,}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with boq_col2:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="card-label">Reinforcement Steel (TMT 500D)</div>
            <div class="card-value" style="font-size:24px;">{mats['steel_tonnes_total']} MT</div>
            <div style="margin-top:8px; font-size:12px; color:#94a3b8;">
                Consumed: <strong style="color:#f59e0b;">{mats['steel_consumed']} MT</strong> | Remaining: <strong style="color:#34d399;">{mats['steel_remaining']} MT</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with boq_col3:
        st.markdown(f"""
        <div class="metric-card-custom">
            <div class="card-label">Ready-Mix Concrete (M25/M30)</div>
            <div class="card-value" style="font-size:24px;">{mats['rmc_m3_total']:,} m³</div>
            <div style="margin-top:8px; font-size:12px; color:#94a3b8;">
                Consumed: <strong style="color:#f59e0b;">{mats['rmc_consumed']:,} m³</strong> | Remaining: <strong style="color:#34d399;">{mats['rmc_remaining']:,} m³</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Conceptual 3D Architectural Rendering via Pollinations AI
    st.markdown("#### 🎨 Conceptual 3D Architectural Rendering (Pollinations AI Integration)")
    st.markdown("Generate real-time conceptual 3D renders of your selected structure type and design parameters using the Pollinations AI prompt generator.")

    render_col1, render_col2 = st.columns([1, 2], gap="medium")

    with render_col1:
        arch_style = st.selectbox(
            "Architectural Design Style",
            ["Modern High-Tech Biophilic", "Contemporary Tropical Brutalist", "Futuristic Parametric Glass", "Minimalist Sustainable Scandinavian", "Industrial High-Bay PEB"],
            index=0
        )
        lighting = st.selectbox(
            "Lighting & Atmosphere",
            ["Dramatic Sunset Golden Hour", "Crisp Morning Architectural Daylight", "Twilight Blue Hour with Exterior Illumination", "Overcast Soft Diffused Sky"],
            index=0
        )

        if st.button("🔄 Generate New 3D Concept Render", type="primary", use_container_width=True):
            st.session_state["render_seed"] += 1
            st.rerun()

    render_url, render_prompt = generate_pollinations_render_url(
        structure_type=selected_structure,
        architectural_style=arch_style,
        lighting_mood=lighting,
        seed=st.session_state["render_seed"]
    )

    with render_col2:
        st.image(render_url, caption=f"3D Render: {selected_structure} ({arch_style})", use_container_width=True)
        with st.expander("🔍 View Generated AI Render Prompt"):
            st.code(render_prompt, language="text")


# ==============================================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER-AWARE ADVISORY (EPIC 5)
# ==============================================================================
with tab4:
    st.markdown("### 🌤️ Daily Site Assistant & Weather-Aware Advisory")
    st.markdown("Dynamic weather safety protocols (crane operations, excavation shoring, concrete curing) and multi-turn technical construction engineering assistant.")

    # Weather Selector Section
    st.markdown("#### 1. Site Weather Condition & Regulatory Safety Protocols")
    selected_weather = st.selectbox(
        "Current Site Weather Forecast Condition",
        options=list(WEATHER_CONDITIONS.keys()),
        index=0
    )

    weather_data = get_weather_protocols(selected_weather)
    w_severity = weather_data.get("severity", "Alert")
    w_color = weather_data.get("color", "#3b82f6")
    w_icon = weather_data.get("icon", "🌤️")

    st.markdown(f"""
    <div style="background:rgba(15, 23, 42, 0.7); border-left:5px solid {w_color}; border-radius:10px; padding:16px 20px; margin:14px 0;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:18px; font-weight:800; color:#f8fafc;">
                {w_icon} {selected_weather}
            </div>
            <span style="background:{w_color}22; color:{w_color}; border:1px solid {w_color}55; padding:4px 12px; border-radius:12px; font-weight:700; font-size:12px;">
                {w_severity}
            </span>
        </div>
        <div style="font-size:13px; color:#a7f3d0; margin-top:10px; background:rgba(6, 78, 59, 0.3); padding:8px 12px; border-radius:6px; border:1px solid rgba(16, 185, 129, 0.2);">
            💧 <strong>Concrete Curing Advisory:</strong> {weather_data.get('curing_notes', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Protocols Grid
    protocols = weather_data.get("protocols", [])
    p_cols = st.columns(len(protocols))
    for i, proto in enumerate(protocols):
        with p_cols[i % len(p_cols)]:
            st.markdown(f"""
            <div style="background:rgba(30, 41, 59, 0.6); border:1px solid rgba(148, 163, 184, 0.15); border-radius:8px; padding:14px; height:100%;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Protocol {i+1}</div>
                <div style="font-weight:700; color:#f1f5f9; font-size:14px; margin:4px 0;">{proto.get('protocol')}</div>
                <div style="font-size:11px; color:#fbbf24; margin-bottom:8px;"><code>{proto.get('code')}</code></div>
                <div style="font-size:12px; color:#cbd5e1;">{proto.get('action')}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Multi-turn Engineering Assistant Chatbot
    st.markdown("#### 2. Interactive Construction Engineering Assistant")
    st.markdown("Ask technical site questions regarding IS 456, OSHA requirements, bar bending schedules, formwork stripping times, or slump test specifications.")

    # Preset Question Quick-Buttons
    st.markdown("<span style='font-size:12px; font-weight:600; color:#94a3b8;'>QUICK CONSULTATION PRESETS:</span>", unsafe_allow_html=True)
    q_cols = st.columns(3)
    for idx, preset_q in enumerate(PRESET_ENGINEERING_PROMPTS[:3]):
        with q_cols[idx]:
            if st.button(f"💬 {preset_q[:42]}...", key=f"preset_btn_{idx}", use_container_width=True):
                st.session_state["chat_history"].append({"role": "user", "content": preset_q})
                with st.spinner("Consulting engineering knowledge base..."):
                    reply = ask_assistant(st.session_state["chat_history"], client)
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                st.rerun()

    # Chat Display Container
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # User Input
    user_prompt = st.chat_input("Enter your structural engineering or safety inquiry (e.g. 'Minimum curing period for OPC vs PPC under IS 456')...")
    if user_prompt:
        st.session_state["chat_history"].append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Formulating technical response under IS / OSHA standards..."):
                assistant_reply = ask_assistant(st.session_state["chat_history"], client)
                st.markdown(assistant_reply)
                st.session_state["chat_history"].append({"role": "assistant", "content": assistant_reply})

    if st.button("🗑️ Clear Chat History", key="clear_chat"):
        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "content": "👋 Chat history cleared. How can I assist you with your construction site operations?"
            }
        ]
        st.rerun()


# ------------------------------------------------------------------------------
# 6. Footer
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 10px 0;">
    <strong>Multimodal Construction Intelligence Platform</strong> | Skill Wallet Capstone Project 1 | Platform ID: <code>6ac4c98d1dcde6d7857c1642</code><br/>
    Built for 1-Click Zero-DB Deployment on Streamlit Community Cloud
</div>
""", unsafe_allow_html=True)
