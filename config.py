"""
Multimodal Construction Intelligence Platform - Configuration & Standards Benchmarks
Platform ID: 6ac4c98d1dcde6d7857c1642 (Skill Wallet Capstone Project 1)
Author: Expert Full-Stack AI Engineer
"""

import os

APP_TITLE = "Multimodal Construction Intelligence Platform"
APP_SUBTITLE = "AI Decision-Support System: Site Safety, Structural Integrity, Material Planning & Weather Advisory"
VERSION = "1.0.0-PROD"

# Default Gemini Models
DEFAULT_VISION_MODEL = "gemini-1.5-flash"
FALLBACK_VISION_MODEL = "gemini-1.5-pro"
DEFAULT_CHAT_MODEL = "gemini-1.5-flash"

# Indian Construction Benchmarks (CPWD, IS 456, RERA Market Benchmarks)
LOCATION_TIERS = {
    "Tier 1 (Metro Hubs)": {
        "cities": ["Mumbai", "Bengaluru", "Delhi NCR", "Hyderabad", "Chennai"],
        "construction_rate_multiplier": 1.25,
        "base_sqft_valuation": 12500,  # INR per sqft market benchmark
        "base_construction_cost": 2750, # INR per sqft standard construction
        "labor_cost_factor": 1.30,
        "safety_compliance_weight": "Strict Urban Municipal Authority (BBMP/BMC/MCD)",
    },
    "Tier 2 (Emerging Capitals)": {
        "cities": ["Pune", "Ahmedabad", "Kolkata", "Kochi", "Jaipur", "Chandigarh"],
        "construction_rate_multiplier": 1.05,
        "base_sqft_valuation": 6800,
        "base_construction_cost": 2250,
        "labor_cost_factor": 1.10,
        "safety_compliance_weight": "Standard State Pollution & RERA Board",
    },
    "Tier 3 (Industrial & Regional Growth)": {
        "cities": ["Indore", "Coimbatore", "Bhopal", "Bhubaneswar", "Lucknow", "Nagpur"],
        "construction_rate_multiplier": 0.90,
        "base_sqft_valuation": 4200,
        "base_construction_cost": 1850,
        "labor_cost_factor": 0.95,
        "safety_compliance_weight": "District Collector & Labor Inspectorate",
    }
}

STRUCTURE_TYPES = {
    "Residential High-Rise (RCC Frame + Mivan)": {
        "cost_multiplier": 1.20,
        "cement_bags_per_sqft": 0.45,
        "steel_kg_per_sqft": 4.5,
        "concrete_m3_per_sqft": 0.042,
        "description": "High-density reinforced concrete shear walls with monolithic aluminum formwork.",
        "prompt_vibe": "Ultra-modern luxury residential skyscraper with cantilevered landscaped balconies, reflective glass curtain walls, golden hour architectural lighting, photorealistic 8k render."
    },
    "Commercial Grade-A Office Complex": {
        "cost_multiplier": 1.45,
        "cement_bags_per_sqft": 0.48,
        "steel_kg_per_sqft": 5.2,
        "concrete_m3_per_sqft": 0.046,
        "description": "Composite structural steel and post-tensioned RCC slabs with high double glazing.",
        "prompt_vibe": "Futuristic commercial corporate headquarters tower with parametric facade, biophilic sky gardens, illuminated glass atrium, architectural photography, dusk elevation."
    },
    "Industrial PEB Warehouse & Logistics Hub": {
        "cost_multiplier": 0.85,
        "cement_bags_per_sqft": 0.32,
        "steel_kg_per_sqft": 3.2,
        "concrete_m3_per_sqft": 0.030,
        "description": "Pre-Engineered Building (PEB) structural steel framing with high-tolerance laser-screed floor slabs.",
        "prompt_vibe": "Massive state-of-the-art automated logistics distribution center, structural steel portal frames, polished concrete flooring, overhead crane gantry, photorealistic isometric architectural cutaway."
    },
    "Luxury Independent Villa / Bungalow": {
        "cost_multiplier": 1.35,
        "cement_bags_per_sqft": 0.42,
        "steel_kg_per_sqft": 4.0,
        "concrete_m3_per_sqft": 0.038,
        "description": "Bespoke architectural RCC frame with premium Italian marble, hardwood facades, and infinity pool.",
        "prompt_vibe": "Contemporary tropical brutalist luxury villa with infinity swimming pool, teak wood louvers, exposed fair-faced concrete, warm ambient lighting, lush tropical landscape, architectural digest cover style."
    },
    "Affordable Housing Monolithic Community": {
        "cost_multiplier": 0.95,
        "cement_bags_per_sqft": 0.38,
        "steel_kg_per_sqft": 3.8,
        "concrete_m3_per_sqft": 0.035,
        "description": "Fast-track monolithic cast-in-place concrete under Pradhan Mantri Awas Yojana (PMAY) norms.",
        "prompt_vibe": "Modern planned urban affordable housing community towers, clean geometric facade with pastel accents, solar rooftop panels, wide pedestrian avenues, bright sunny day rendering."
    }
}

# Weather Advisory Matrix & Regulatory Safety Thresholds
WEATHER_CONDITIONS = {
    "High Wind (> 38 km/h / 20 knots)": {
        "icon": "💨",
        "severity": "High Alert",
        "color": "#F59E0B",
        "protocols": [
            {"protocol": "Tower Crane Suspension", "code": "IS 875 (Part 3) & OSHA 1926.1431", "action": "Halt all tower crane, mobile boom, and suspended cradle operations immediately. Park jib in free-wheeling (weathervane) condition."},
            {"protocol": "Scaffolding Plank Anchoring", "code": "IS 3696 / OSHA 1926.451", "action": "Inspect and tie down all loose metallic/wooden planks, safety netting, and debris sheets on external perimeter scaffolding."},
            {"protocol": "Glazing & External Cladding", "code": "National Building Code (NBC) 2016", "action": "Cease all external glass curtain wall installations and façade cradling work at heights exceeding 10 meters."}
        ],
        "curing_notes": "Rapid surface moisture evaporation risk. Apply curing compound immediately following formwork stripping to avoid plastic shrinkage cracking."
    },
    "Heavy Rain / Monsoon Inundation": {
        "icon": "🌧️",
        "severity": "Critical Alert",
        "color": "#EF4444",
        "protocols": [
            {"protocol": "Basement Trench & Excavation Shoring", "code": "IS 3764 & OSHA 1926.651", "action": "Suspend excavation deeper than 1.5m. Verify sheet pile and soil nail stability. Keep 24/7 dewatering diesel pumps online."},
            {"protocol": "Electrical Lockout/Tagout (LOTO)", "code": "IS 13416 Part 5 / OSHA 1926.404", "action": "De-energize temporary electrical feeder boards, portable welding transformers, and cables submerged in standing puddle water."},
            {"protocol": "RCC Concrete Pour Protection", "code": "IS 456:2000 Clause 14", "action": "Do not pour unshielded concrete in active downpours. Cover freshly laid structural slabs with waterproof polyethylene sheets to avoid water-cement dilution."}
        ],
        "curing_notes": "Natural ambient moisture aids hydration; however, continuous pooling can leach calcium hydroxide. Provide adequate slope drainage."
    },
    "Extreme Heat (> 40°C / Hot Weather Concreting)": {
        "icon": "☀️",
        "severity": "Moderate Warning",
        "color": "#EA580C",
        "protocols": [
            {"protocol": "Hot Weather Concrete Pouring", "code": "IS 7861 (Part 1) & ACI 305R", "action": "Reschedule major slab pours to twilight/night shifts. Pre-cool aggregate piles, use chilled batching water or crushed ice flakes to keep fresh concrete < 32°C."},
            {"protocol": "Worker Thermal Hydration Program", "code": "OSHA Safety & Health Regulations Part 1926", "action": "Enforce mandatory 15-minute rest rotations every 45 minutes in shaded ventilation booths. Provide electrolyte ORS stations."},
            {"protocol": "Immediate Moist Curing Initiation", "code": "IS 456:2000 Clause 13.5", "action": "Commence continuous ponding or saturated hessian/burlap wrapping within 2 hours of concrete final setting to mitigate thermal shrinkage stresses."}
        ],
        "curing_notes": "Minimum continuous water curing duration must be extended to 14 days for mineral-admixture/fly-ash blended cements."
    },
    "Normal Weather (Optimal Site Conditions)": {
        "icon": "🌤️",
        "severity": "Optimal Operational State",
        "color": "#10B981",
        "protocols": [
            {"protocol": "Standard PPE Mandate Compliance", "code": "IS 2925, IS 15298, OSHA 1926.95", "action": "Enforce 100% hard hat, hi-vis vest, steel-toe boots, and chin-strap retention across all active work zones."},
            {"protocol": "Rebar Shuttering Clearance Inspection", "code": "IS 456 Clause 26.4", "action": "Verify concrete clear cover blocks (25mm slab, 40mm column/beam, 50mm footing) prior to issuing pouring permit."},
            {"protocol": "Routine Structural Defect Audit", "code": "CPWD Quality Control Manual", "action": "Conduct daily visual and photographic walk-through of stripped formwork for honeycombing, spalling, or micro-cracks."}
        ],
        "curing_notes": "Standard 7-day ponding for Ordinary Portland Cement (OPC) and 10 days for mineral admixed/pozzolanic concrete."
    }
}

# Preset Prompts for Assistant
PRESET_ENGINEERING_PROMPTS = [
    "What is the minimum curing period for OPC vs PPC concrete under IS 456:2000?",
    "Permissible crack width limits for RCC members in severe exposure environments?",
    "OSHA fall protection requirements for scaffoldings above 10 feet?",
    "How to mitigate plastic shrinkage cracking in hot weather concreting (IS 7861)?",
    "Thumb-rule calculations for steel reinforcement density in residential columns?"
]
