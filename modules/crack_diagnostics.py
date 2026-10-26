"""
Epic 2: Concrete Crack Diagnostics & Structural Integrity Module
Classifies structural concrete defects and prescribes engineering remediation.
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

from typing import Dict, Any, Optional
from PIL import Image
from modules.gemini_client import GeminiConstructionClient


CRACK_DIAGNOSTICS_SYSTEM_PROMPT = """
You are a Senior Forensic Structural Engineer and Concrete Technologist specialized in Non-Destructive Testing (NDT), crack diagnostics, and rehabilitation under IS 456:2000, ACI 224.1R, and BS 8110 standards.
Your role is to analyze concrete and masonry defect photographs, classify the failure mechanism, gauge crack width (mm), determine structural safety implications, and specify precise repair engineering methodologies.

Return ONLY structured JSON conforming to the requested schema.
"""

CRACK_DIAGNOSTICS_USER_PROMPT = """
Inspect this image of a structural concrete or masonry surface.
Analyze the visible defect, classifying it into one of the following primary categories:
1. Hairline Crack (Plastic Shrinkage / Micro-crazing)
2. Settlement Crack (Differential Foundation Movement)
3. Structural Shear Crack (Diagonal tension, 45-degree beam/column load stress)
4. Thermal Expansion / Contraction Crack (Seasonal cyclical stress)
5. Spalling & Rebar Delamination (Chloride attack, carbonation, corrosion expansive pressure)

Estimate the crack width in millimeters (mm), state root cause, assign structural urgency, and prescribe remedial engineering protocols (e.g. low-viscosity epoxy pressure injection, polyurethane chemical grouting, carbon fiber composite wrapping, rebar rust converter treatment, stitching).

Respond with ONLY valid JSON with this exact schema:
{
  "defect_type": "<Hairline | Settlement | Structural Shear | Thermal Expansion | Spalling & Rebar Corrosion>",
  "estimated_crack_width_mm": <number in mm, e.g. 1.85>,
  "confidence_score": <number between 0 and 100>,
  "urgency": "<Immediate Evacuation & Shoring | High - Urgent Repair (Within 7 Days) | Moderate - Monitor & Seal (Within 30 Days) | Low - Cosmetic Maintenance>",
  "structural_integrity_score": <number between 0 and 100 representing health of member, 100 being pristine>,
  "affected_element": "<e.g. RCC Column Joint | Cantilever Beam Midspan | Retaining Wall | Floor Slab Plinth>",
  "primary_failure_mechanism": "<Brief explanation of how the crack formed>",
  "root_causes": [
    "<Primary root cause>",
    "<Contributing environmental or loading factor>"
  ],
  "governing_standard_compliance": {
    "is_code": "IS 456:2000 Clause 35.3.2 Limit State of Serviceability",
    "permissible_width_limit_mm": <e.g. 0.20 or 0.30>,
    "compliance_status": "<Within Permissible Tolerance | Exceeds Permissible Tolerance - Violation>"
  },
  "recommended_engineering_repairs": [
    {
      "step": 1,
      "method": "<e.g. V-Groove Routing & Surface Preparation>",
      "specification": "<Material & application specification, e.g. diamond saw chase 15mm x 15mm>",
      "material_grade": "<e.g. Polymer Modified Mortar (PMM) / Solvent-free primer>"
    },
    {
      "step": 2,
      "method": "<e.g. Low-Viscosity Epoxy Pressure Grouting>",
      "specification": "<Packer spacing, pressure limit e.g. 2.5 bar, viscosity < 150 cP>",
      "material_grade": "<e.g. ASTM C881 Type I/IV Grade 1 Epoxy Resin>"
    },
    {
      "step": 3,
      "method": "<e.g. Structural Strengthening / Fiber Wrap (if required)>",
      "specification": "<e.g. Unidirectional Carbon Fiber Reinforced Polymer (CFRP) fabric wrap>",
      "material_grade": "<e.g. 300 gsm High-Tensile Modulus Carbon Fabric>"
    }
  ],
  "monitoring_advisory": "<Advisory on installing optical tell-tale crack gauges or ultrasonic pulse velocity (UPV) test>"
}
"""


def run_crack_diagnostics(image: Image.Image, client: GeminiConstructionClient) -> Dict[str, Any]:
    """
    Executes multimodal concrete defect classification.
    Falls back gracefully to authentic structural engineering data in demo mode.
    """
    if not client.is_demo_mode():
        result, error = client.analyze_image_multimodal(
            image=image,
            prompt=CRACK_DIAGNOSTICS_USER_PROMPT,
            system_instruction=CRACK_DIAGNOSTICS_SYSTEM_PROMPT
        )
        if result and "defect_type" in result:
            result["_source"] = "Live Multimodal AI (Google Gemini 1.5)"
            result["_is_live"] = True
            return result
        simulated = get_simulated_crack_diagnostics()
        simulated["_source"] = f"Demonstration Fallback (API Notice: {error or 'Response format variance'})"
        simulated["_is_live"] = False
        return simulated

    # Authentic high-fidelity forensic demo report
    simulated = get_simulated_crack_diagnostics()
    simulated["_source"] = "Demonstration Mode (IS 456 & ACI Structural Benchmarks)"
    simulated["_is_live"] = False
    return simulated


def get_simulated_crack_diagnostics() -> Dict[str, Any]:
    """Provides a realistic forensic engineering defect report for demonstration."""
    return {
        "defect_type": "Structural Shear Crack",
        "estimated_crack_width_mm": 1.75,
        "confidence_score": 94,
        "urgency": "High - Urgent Repair (Within 7 Days)",
        "structural_integrity_score": 58,
        "affected_element": "Reinforced Concrete Beam-Column Shear Span",
        "primary_failure_mechanism": "Diagonal tension cracking propagating at approximately 45 degrees towards the support due to principal tensile stresses exceeding concrete shear capacity.",
        "root_causes": [
            "Inadequate shear stirrup spacing (two-legged stirrups exceeding d/2 limit under IS 456 Cl 26.5.1.5).",
            "Unforeseen live load surcharge on upper floor slab exceeding design assumptions.",
            "Micro-settlement at the column footing accentuating differential torsional shear."
        ],
        "governing_standard_compliance": {
            "is_code": "IS 456:2000 Clause 35.3.2 Limit State of Serviceability (Cracking)",
            "permissible_width_limit_mm": 0.20,
            "compliance_status": "Exceeds Permissible Tolerance - Critical Violation (1.75mm vs 0.20mm limit)"
        },
        "recommended_engineering_repairs": [
            {
                "step": 1,
                "method": "Temporary Shoring & Load Relief",
                "specification": "Install adjustable Acrow steel props with timber sole plates beneath the affected beam span to relieve 70% live load before grouting.",
                "material_grade": "Heavy-Duty IS 1161 Steel Tubular Props"
            },
            {
                "step": 2,
                "method": "V-Cut Routing & Surface Port Fixing",
                "specification": "Chase out a 20mm x 20mm V-groove along the crack line; clean with oil-free compressed air; seal surface with rapid-set epoxy putty and install brass injection nipples at 200mm centers.",
                "material_grade": "Thixotropic Epoxy Adhesive (ASTM C881 Grade 3)"
            },
            {
                "step": 3,
                "method": "Low-Viscosity Epoxy Pressure Injection",
                "specification": "Inject ultra-low viscosity resin starting from bottom port upwards until resin purges freely from adjacent nipple. Maintain 2 to 3 bar sustained pressure.",
                "material_grade": "Solvent-free High-Modulus Epoxy (Viscosity < 120 mPa·s, Compressive Strength > 75 N/mm²)"
            },
            {
                "step": 4,
                "method": "CFRP Composite Shear Strengthening",
                "specification": "Apply 2 layers of unidirectional Carbon Fiber Reinforced Polymer (CFRP) U-jacketing around beam sides and soffit to restore shear capacity up to 140% of original design.",
                "material_grade": "300 gsm High-Modulus Carbon Fabric with Saturant Epoxy"
            }
        ],
        "monitoring_advisory": "Affix calibrated 2D Avongard acrylic tell-tale crack motion gauges across the injected fissure. Perform Ultrasonic Pulse Velocity (UPV) grid testing (IS 13311 Part 1) at 14 days to confirm deep resin penetration."
    }
