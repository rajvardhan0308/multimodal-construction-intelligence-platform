"""
Epic 3: Planning & Real Estate Valuation Module
Calculates project budget, CapEx, INR market valuation, material quantities,
and generates conceptual 3D architectural renders via Pollinations AI.
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import urllib.parse
from typing import Dict, Any, Tuple
from config import LOCATION_TIERS, STRUCTURE_TYPES


def calculate_project_metrics(
    structure_type: str,
    built_up_sqft: float,
    location_tier: str,
    completion_percentage: float
) -> Dict[str, Any]:
    """
    Computes comprehensive civil engineering quantities, financial budgets,
    CapEx spent, and current Indian real estate market asset valuation.
    """
    tier_info = LOCATION_TIERS.get(location_tier, list(LOCATION_TIERS.values())[0])
    struct_info = STRUCTURE_TYPES.get(structure_type, list(STRUCTURE_TYPES.values())[0])

    # 1. Base Construction Cost Calculation
    base_cost_per_sqft = tier_info["base_construction_cost"] * struct_info["cost_multiplier"]
    total_project_budget_inr = built_up_sqft * base_cost_per_sqft

    # 2. Capital Expenditure Incurred
    # Slightly non-linear S-curve frontloaded for foundation/RCC frame
    progress_ratio = completion_percentage / 100.0
    capex_incurred_inr = total_project_budget_inr * progress_ratio

    # 3. Real Estate Market Asset Valuation (INR)
    # Valuation considers land + constructed asset premium.
    # At 0% completion, land value represents ~40% of future finished value.
    # As completion advances towards 100%, risk discounts diminish and market asset value scales.
    market_rate_per_sqft = tier_info["base_sqft_valuation"] * struct_info["cost_multiplier"]
    full_completed_market_value = built_up_sqft * market_rate_per_sqft

    # Asset valuation at current stage
    # Base land equity (35%) + Work in Progress equity (65% * completion_ratio)
    current_asset_valuation_inr = full_completed_market_value * (0.35 + 0.65 * progress_ratio)

    # 4. Quantity Surveying & Material Estimations (IS 456 & CPWD Thumb Rules)
    cement_bags_total = built_up_sqft * struct_info["cement_bags_per_sqft"]
    steel_tonnes_total = (built_up_sqft * struct_info["steel_kg_per_sqft"]) / 1000.0
    rmc_m3_total = built_up_sqft * struct_info["concrete_m3_per_sqft"]

    # Materials consumed vs remaining based on completion %
    cement_consumed = cement_bags_total * progress_ratio
    steel_consumed = steel_tonnes_total * progress_ratio
    rmc_consumed = rmc_m3_total * progress_ratio

    # Formatting INR to Crores and Lakhs
    def format_inr(amount: float) -> str:
        crores = amount / 10000000.0
        if crores >= 1.0:
            return f"₹{crores:.2f} Cr"
        else:
            lakhs = amount / 100000.0
            return f"₹{lakhs:.2f} Lakhs"

    # Milestone breakdown
    milestones = [
        {"name": "Substructure & Foundation", "weight": 20, "status": "Completed" if completion_percentage >= 20 else ("In Progress" if completion_percentage > 0 else "Pending")},
        {"name": "RCC Superstructure Frame", "weight": 35, "status": "Completed" if completion_percentage >= 55 else ("In Progress" if completion_percentage > 20 else "Pending")},
        {"name": "Masonry, AAC Blocks & Rough MEP", "weight": 20, "status": "Completed" if completion_percentage >= 75 else ("In Progress" if completion_percentage > 55 else "Pending")},
        {"name": "Façade, Flooring & Internal Finishing", "weight": 15, "status": "Completed" if completion_percentage >= 90 else ("In Progress" if completion_percentage > 75 else "Pending")},
        {"name": "Commissioning, Testing & Handover", "weight": 10, "status": "Completed" if completion_percentage >= 100 else ("In Progress" if completion_percentage > 90 else "Pending")},
    ]

    return {
        "built_up_sqft": built_up_sqft,
        "structure_type": structure_type,
        "location_tier": location_tier,
        "completion_percentage": completion_percentage,
        "construction_rate_per_sqft": round(base_cost_per_sqft),
        "total_budget_inr": total_project_budget_inr,
        "total_budget_formatted": format_inr(total_project_budget_inr),
        "capex_incurred_inr": capex_incurred_inr,
        "capex_incurred_formatted": format_inr(capex_incurred_inr),
        "capex_remaining_formatted": format_inr(total_project_budget_inr - capex_incurred_inr),
        "current_valuation_inr": current_asset_valuation_inr,
        "current_valuation_formatted": format_inr(current_asset_valuation_inr),
        "completed_valuation_formatted": format_inr(full_completed_market_value),
        "materials": {
            "cement_bags_total": round(cement_bags_total),
            "cement_consumed": round(cement_consumed),
            "cement_remaining": round(cement_bags_total - cement_consumed),
            "steel_tonnes_total": round(steel_tonnes_total, 1),
            "steel_consumed": round(steel_consumed, 1),
            "steel_remaining": round(steel_tonnes_total - steel_consumed, 1),
            "rmc_m3_total": round(rmc_m3_total),
            "rmc_consumed": round(rmc_consumed),
            "rmc_remaining": round(rmc_m3_total - rmc_consumed)
        },
        "milestones": milestones
    }


def generate_pollinations_render_url(
    structure_type: str,
    architectural_style: str = "Modern High-Tech Biophilic",
    lighting_mood: str = "Dramatic Sunset Golden Hour",
    width: int = 1024,
    height: int = 768,
    seed: int = 42
) -> Tuple[str, str]:
    """
    Constructs an AI image generation prompt and returns a direct Pollinations AI URL
    and the text prompt used for transparency.
    """
    struct_info = STRUCTURE_TYPES.get(structure_type, list(STRUCTURE_TYPES.values())[0])
    base_vibe = struct_info.get("prompt_vibe", "Ultra-modern architectural masterpiece")

    full_prompt = (
        f"Award-winning architectural 3D conceptual rendering of {structure_type}, "
        f"design style {architectural_style}, lighting: {lighting_mood}, {base_vibe}, "
        f"photorealistic, Octane render, unreal engine 5, ray tracing, ultra detailed 8k elevation, "
        f"landscaped surroundings, civil engineering showcase"
    )

    encoded_prompt = urllib.parse.quote_plus(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
    return url, full_prompt
