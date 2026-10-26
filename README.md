# 🏗️ Multimodal Construction Intelligence Platform
### Skill Wallet Capstone Project 1 | Platform ID: `6ac4c98d1dcde6d7857c1642`
**Category:** Generative AI | Real Estate Decision Support  
**Target Deployment:** Streamlit Community Cloud (Zero-Database Serverless Architecture)

---

## 🌟 Executive Overview
The **Multimodal Construction Intelligence Platform** is an enterprise-grade decision-support system designed for civil contractors, structural consultants, and real estate developers. Grounded in **OSHA 29 CFR 1926**, **IS 456:2000**, and **Bureau of Indian Standards (BIS)**, the platform fuses multimodal vision intelligence, automated quantity surveying, real estate valuation models, and dynamic weather hazard mitigations into a seamless single-click web application.

---

## 📐 Architecture & Epic Coverage Matrix

| Epic | Module Name | Core Capabilities | Regulatory / Technical Standard |
|---|---|---|---|
| **Epic 1** | **Requirements & Environment** | Zero-DB serverless architecture, dual runtime (Live Gemini 1.5 vs Demonstration Mode fallback). | Python 3.9+, Streamlit, Pillow |
| **Epic 2** | **Site Safety & PPE Audit** | Multimodal scan for hard hats, high-vis vests, steel-toe footwear, and full-body harnesses. Outputs composite Safety Score (0-100), hazard logs, and remedial steps. | OSHA 29 CFR 1926, IS 2925, IS 15809, IS 15298, IS 3521 |
| **Epic 2** | **Crack Diagnostics & Integrity** | Classifies fissures (Hairline, Settlement, Structural Shear, Thermal, Spalling). Computes crack width (mm), failure kinematics, and prescribes ASTM/IS repair steps. | IS 456:2000 Cl. 35.3.2, ACI 224.1R, BS 8110 |
| **Epic 3** | **Planning & Valuation** | Interactive inputs for structure type, built-up sqft, Tier 1/2/3 Indian cities, milestone progress. Computes INR budget, CapEx spent, market asset valuation, and cement/steel/RMC BOQ. | CPWD Schedule of Rates, Indian RERA Market Valuation Benchmarks |
| **Epic 3** | **3D Architectural Concept Renders** | Real-time generative architectural visualization prompt generator and rendering engine via Pollinations AI. | Pollinations / Flux AI Integration |
| **Epic 5** | **Weather Advisory & Safety Protocols** | Weather-aware hazard rules (High Wind crane halts, Heavy Rain LOTO & dewatering, Extreme Heat hot-weather concreting & curing protocols). | IS 875 (Part 3), IS 7861 (Part 1), OSHA 1926.1431 |
| **Epic 5** | **Engineering Assistant Chatbot** | Multi-turn conversational civil engineering agent answering technical questions on codes, curing times, rebar ratios, and inspection checklists. | Grounded in IS 456, OSHA, and CPWD Works Manual |
| **Epic 6** | **Interface, Testing & Deployment** | Modern dark-themed glassmorphic UI, responsive metric cards, status pills, downloadable JSON reports, 100% cloud-ready. | Streamlit Community Cloud (share.streamlit.io) |

---

## 🚀 Key Features Walkthrough

### 1. Dual Execution Mode (With or Without API Key)
- **Live Multimodal Mode:** Enter any valid Google Gemini API key in the sidebar for live multimodal visual inspection and dynamic LLM reasoning.
- **Graceful Demonstration Fallback:** If no API key is supplied, the platform automatically engages its pre-calibrated engineering benchmark engine. Built-in sample inspection images allow instant 1-click evaluation without external dependencies.

### 2. Tab 1: Site Safety & PPE Audit
- Supports JPG/PNG photo uploads.
- Detects worker PPE compliance: Safety Helmets, High-Vis Vests, Steel-Toe Boots, and Safety Harnesses.
- Generates structured JSON reports with severity levels (`Critical`, `High`, `Medium`, `Low`) and OSHA/IS code violations.
- Includes 1-Click JSON export.

### 3. Tab 2: Concrete Crack Diagnostics & Structural Integrity
- Classifies concrete defect types with estimated crack width (mm).
- Evaluates compliance against IS 456 permissible crack width limits (0.20 mm for moderate exposure).
- Outlines multi-phase repair engineering protocols (e.g., temporary shoring, V-cut routing, low-viscosity epoxy pressure injection, CFRP carbon fiber strengthening).

### 4. Tab 3: Planning, BOQ Estimations & Real Estate Valuation
- Dynamic calculations tailored to Indian city tiers:
  - **Tier 1:** Mumbai, Bengaluru, Delhi NCR, Hyderabad, Chennai
  - **Tier 2:** Pune, Ahmedabad, Kolkata, Kochi, Jaipur, Chandigarh
  - **Tier 3:** Indore, Coimbatore, Bhopal, Bhubaneswar, Lucknow, Nagpur
- Calculates Total Project Budget, CapEx Incurred, Current Valuation, and Projected Finished Market Value in **INR Lakhs/Crores**.
- Quantifies cement bags (50kg), reinforcement steel (MT), and RMC (m³).
- Generates real-time 3D conceptual architectural renders via Pollinations AI.

### 5. Tab 4: Weather-Aware Advisory & Engineering Chatbot
- Select from **High Wind (> 38 km/h)**, **Heavy Rain / Monsoon**, **Extreme Heat (> 40°C)**, and **Normal Weather**.
- Enforces regulatory protocols: crane boom weathervaning, electrical LOTO, trench dewatering, and concrete curing durations.
- Interactive multi-turn AI chatbot with quick-consultation preset engineering questions.

---

## 📦 Directory Structure
```
multimodal_construction_platform/
├── app.py                      # Main Streamlit application
├── config.py                   # Indian construction standards & pricing benchmarks
├── requirements.txt            # Python production dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Complete architectural documentation
├── assets/
│   ├── styles.css              # Modern glassmorphism CSS design system
│   ├── sample_site_safety.jpg  # Built-in sample site inspection photo
│   └── sample_concrete_crack.jpg # Built-in sample concrete crack photo
└── modules/
    ├── __init__.py
    ├── gemini_client.py        # Gemini multimodal client & demo fallback engine
    ├── safety_audit.py         # Epic 2: PPE audit & OSHA/IS hazard analyzer
    ├── crack_diagnostics.py    # Epic 2: Concrete crack classification & repair
    ├── planning_valuation.py   # Epic 3: Cost estimation, BOQ & Pollinations AI
    └── weather_advisory.py     # Epic 5: Weather protocols & civil assistant
```

---

## 💻 Local Quickstart

### Prerequisites
- Python 3.9, 3.10, 3.11, 3.12, or 3.13
- Git

### 1. Clone or Navigate to the Repository
```bash
git clone https://github.com/pushkar-singh-dev/multimodal-construction-intelligence-platform.git
cd multimodal-construction-intelligence-platform
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ 1-Click Streamlit Community Cloud Deployment
To fulfill **Step 33 (GitHub Link)** and **Step 34 (Live Demo Link)** on Skill Wallet:

1. **Push to GitHub**:
   - Create a new public repository on GitHub (e.g. `multimodal-construction-intelligence-platform`).
   - Push this codebase to the repository on branch `main`.
2. **Deploy on Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io).
   - Sign in with your GitHub account.
   - Click **"New app"**.
   - Select your repository: `multimodal-construction-intelligence-platform`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - *(Optional)* In Advanced Settings > Secrets, add `GEMINI_API_KEY = "your_key"`.
   - Click **"Deploy!"**.
3. **Submit on Skill Wallet**:
   - In **Step 33**, paste your GitHub repository link.
   - In **Step 34**, paste your live deployed URL (e.g., `https://<your-app>.streamlit.app`).

---

## 📜 Regulatory Standards Reference
- **OSHA 29 CFR 1926**: Safety and Health Regulations for Construction
- **IS 456:2000**: Code of Practice for Plain and Reinforced Concrete
- **IS 875 (Part 3):2015**: Design Loads (Wind Loads) for Buildings and Structures
- **IS 13416**: Recommendations for Preventive Measures Against Hazards at Work Places
- **IS 7861 (Part 1 & 2)**: Code of Practice for Extreme Weather Concreting
- **CPWD Analysis of Rates & Works Manual**: Central Public Works Department Benchmarks

---
**Skill Wallet Capstone Project 1** | *Designed & Engineered for Production Deployment*
