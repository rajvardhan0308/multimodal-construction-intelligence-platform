"""
Epic 2: Site Safety & PPE Audit Module
Analyzes worker PPE compliance under OSHA (29 CFR 1926) & IS 456 / IS 13416 / IS 3696 Standards.
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

from typing import Dict, Any, Optional
from PIL import Image
from modules.gemini_client import GeminiConstructionClient


SAFETY_AUDIT_SYSTEM_PROMPT = """
You are a Principal OSHA Safety Inspector and Bureau of Indian Standards (BIS / IS 456 / IS 13416) Chief Auditor for Mega Civil Infrastructure.
Your role is to perform rigorous multimodal visual audits on construction site photographs to detect worker Personal Protective Equipment (PPE) compliance, unsafe site practices, and structural safety hazards.

You must return ONLY a structured JSON document conforming strictly to the requested schema.
"""

SAFETY_AUDIT_USER_PROMPT = """
Inspect this construction site image thoroughly. Detect all visible workers, assess their PPE gear compliance against OSHA 29 CFR 1926 and Indian National Building Code / IS standards (IS 2925 for hard hats, IS 15809 for high-vis, IS 15298 for safety shoes, IS 3521 for safety harnesses).

Identify any open hazards such as unprotected floor edges, missing guardrails, unshielded rebar, ladder violations, overhead lifting risks, or electrical dangers.

Respond with ONLY valid JSON with this exact schema:
{
  "safety_score": <number between 0 and 100>,
  "overall_status": "<Compliant | Warning - Partial Compliance | Critical Non-Compliance>",
  "audit_timestamp": "ISO-8601 string",
  "summary": "<Concise 2-3 sentence executive safety summary of the site>",
  "workers_detected_count": <integer count of workers seen>,
  "ppe_detection": [
    {
      "item": "Safety Helmets (Hard Hats)",
      "status": "<Compliant | Partial | Non-Compliant | Not Applicable>",
      "detected_count": <number compliant>,
      "total_workers": <number required>,
      "governing_standard": "IS 2925 / OSHA 1926.100",
      "observations": "<specific observations on chin-straps, proper fitting, or workers without hats>"
    },
    {
      "item": "High-Visibility Vests",
      "status": "<Compliant | Partial | Non-Compliant | Not Applicable>",
      "detected_count": <number compliant>,
      "total_workers": <number required>,
      "governing_standard": "IS 15809 / OSHA 1926.201",
      "observations": "<observations on retroreflective tape and daylight visibility>"
    },
    {
      "item": "Steel-Toe Safety Footwear",
      "status": "<Compliant | Partial | Non-Compliant | Not Applicable>",
      "detected_count": <number compliant>,
      "total_workers": <number required>,
      "governing_standard": "IS 15298 / OSHA 1926.96",
      "observations": "<observations on puncture-resistant soles and toe protection>"
    },
    {
      "item": "Safety Harnesses & Fall Arrest",
      "status": "<Compliant | Partial | Non-Compliant | Not Applicable>",
      "detected_count": <number compliant>,
      "total_workers": <number required>,
      "governing_standard": "IS 3521 / OSHA 1926.502",
      "observations": "<observations on 100% tie-off, lanyard condition, and static lifeline anchoring>"
    }
  ],
  "identified_site_hazards": [
    {
      "hazard_id": "HAZ-001",
      "title": "<Name of hazard, e.g. Unprotected Slab Edge at Height>",
      "severity": "<Critical | High | Medium | Low>",
      "location_zone": "<Zone in image, e.g. Upper Left Floor Perimeter>",
      "osha_violation": "<e.g. OSHA 1926.501(b)(1) - Unprotected sides and edges>",
      "is_standard": "<e.g. IS 13416 (Part 2) - Precautions for perimeter falls>",
      "corrective_remedy": "<Immediate actionable engineering fix or procedural mitigation>"
    }
  ],
  "immediate_remedial_actions": [
    "<Step 1 action>",
    "<Step 2 action>",
    "<Step 3 action>"
  ]
}
"""


def run_safety_audit(image: Image.Image, client: GeminiConstructionClient) -> Dict[str, Any]:
    """
    Executes the multimodal safety audit.
    If client is in demo mode or API fails, returns an authentic, structured demo audit.
    """
    if not client.is_demo_mode():
        result, error = client.analyze_image_multimodal(
            image=image,
            prompt=SAFETY_AUDIT_USER_PROMPT,
            system_instruction=SAFETY_AUDIT_SYSTEM_PROMPT
        )
        if result and "safety_score" in result:
            result["_source"] = "Live Multimodal AI (Google Gemini 1.5)"
            result["_is_live"] = True
            return result
        simulated = get_simulated_safety_audit()
        simulated["_source"] = f"Demonstration Fallback (API Notice: {error or 'Response format variance'})"
        simulated["_is_live"] = False
        return simulated

    # High-fidelity domain demonstration audit
    simulated = get_simulated_safety_audit()
    simulated["_source"] = "Demonstration Mode (Built-in IS 456 / OSHA Benchmarks)"
    simulated["_is_live"] = False
    return simulated


def get_simulated_safety_audit() -> Dict[str, Any]:
    """Provides an authentic, regulatory-grade safety audit payload for demo purposes."""
    return {
        "safety_score": 68,
        "overall_status": "Warning - Action Required",
        "audit_timestamp": "2026-10-25T11:45:00Z",
        "summary": "Visual scan indicates moderate site compliance. Primary personnel exhibit hard hat adherence, but critical fall arrest violations and missing edge guardrails are observed on elevated formwork decking.",
        "workers_detected_count": 4,
        "ppe_detection": [
            {
                "item": "Safety Helmets (Hard Hats)",
                "status": "Compliant",
                "detected_count": 4,
                "total_workers": 4,
                "governing_standard": "IS 2925:1984 / OSHA 1926.100",
                "observations": "All 4 active workers are wearing high-impact industrial safety helmets; chin-straps fastened."
            },
            {
                "item": "High-Visibility Vests",
                "status": "Partial",
                "detected_count": 3,
                "total_workers": 4,
                "governing_standard": "IS 15809:2008 / OSHA 1926.201",
                "observations": "3 workers wearing Class 2 high-vis reflective vests. 1 helper in center scaffold zone lacks fluorescent PPE."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "status": "Compliant",
                "detected_count": 4,
                "total_workers": 4,
                "governing_standard": "IS 15298 / OSHA 1926.96",
                "observations": "Workers wearing heavy-duty ankle-height safety footwear with puncture-resistant steel midsole inserts."
            },
            {
                "item": "Safety Harnesses & Fall Arrest",
                "status": "Non-Compliant",
                "detected_count": 0,
                "total_workers": 2,
                "governing_standard": "IS 3521 / OSHA 1926.502",
                "observations": "Two workers operating near leading deck slab edge (> 3.5m height) have no full-body harness tied off to lifelines."
            }
        ],
        "identified_site_hazards": [
            {
                "hazard_id": "HAZ-001",
                "title": "Unprotected Slab Edge & Missing Guardrails",
                "severity": "Critical",
                "location_zone": "Upper Concrete Floor Perimeter (Right Quadrant)",
                "osha_violation": "OSHA 1926.501(b)(1) - Unprotected sides and edges 6ft+ above lower level",
                "is_standard": "IS 13416 (Part 2) - Safety precautions during construction of building",
                "corrective_remedy": "Immediately halt work on slab edge. Install 1.05m standard double-tier guardrails with mid-rails and 150mm toe-boards, or install horizontal static life-wire."
            },
            {
                "hazard_id": "HAZ-002",
                "title": "Uncapped Vertical Reinforcement Starter Bars (Impaling Hazard)",
                "severity": "High",
                "location_zone": "Lower Column Foundation Section",
                "osha_violation": "OSHA 1926.701(b) - Reinforcing steel impalement protection",
                "is_standard": "IS 456:2000 Section 2 - General Construction Practice",
                "corrective_remedy": "Cap all exposed vertical TMT rebar ends with OSHA-approved mushroom caps or secure wooden trough capping."
            },
            {
                "hazard_id": "HAZ-003",
                "title": "Temporary Electrical Feeder Line across Wet Walkway",
                "severity": "Medium",
                "location_zone": "Ground Level Material Transit Corridor",
                "osha_violation": "OSHA 1926.404(b)(1) - Ground fault protection",
                "is_standard": "IS 13416 (Part 5) - Electrical hazards at construction sites",
                "corrective_remedy": "Elevate temporary three-phase cables onto insulated timber poles at 2.4m clearance or route through heavy-duty PVC ducting."
            }
        ],
        "immediate_remedial_actions": [
            "Issue Stop-Work Notice on Level 3 leading slab edge until fall arrest static lines and double guardrails are bolted.",
            "Deploy OSHA mushroom rebar caps across column starter cages before next concrete batching.",
            "Dispatch Safety Officer for daily Toolbox Talk covering 100% harness hook-off and high-vis vest compliance."
        ]
    }
