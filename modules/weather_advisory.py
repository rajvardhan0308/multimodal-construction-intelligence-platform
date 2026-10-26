"""
Epic 5: Weather-Aware Advisory & Interactive Construction Engineering Assistant
Provides weather hazard mitigations and multi-turn technical chatbot grounded in IS codes and OSHA.
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

from typing import Dict, Any, List
from config import WEATHER_CONDITIONS, PRESET_ENGINEERING_PROMPTS
from modules.gemini_client import GeminiConstructionClient


ENGINEERING_ASSISTANT_SYSTEM_CONTEXT = """
You are the Chief Structural & Safety Advisory AI on a major construction project.
Your knowledge base is anchored in:
- Indian Standard Codes: IS 456:2000 (Plain and Reinforced Concrete), IS 875 (Wind & Design Loads), IS 3696 (Scaffolds and Ladders), IS 13416 (Construction Safety Recommendations), IS 7861 (Hot & Cold Weather Concreting).
- OSHA Regulations: 29 CFR 1926 (Safety and Health Regulations for Construction), Subpart M (Fall Protection), Subpart CC (Cranes and Derricks), Subpart P (Excavations).
- CPWD Works Manual & Specifications.

Answer with crisp, authoritative civil engineering accuracy. State exact code clauses, numerical safety factors, curing durations, or structural dimensions where applicable. Always prioritize site life-safety.
"""


def get_weather_protocols(condition_name: str) -> Dict[str, Any]:
    """Retrieves standard safety protocols and curing advisories for the given weather condition."""
    return WEATHER_CONDITIONS.get(condition_name, WEATHER_CONDITIONS["Normal Weather (Optimal Site Conditions)"])


def ask_assistant(
    messages: List[Dict[str, str]],
    client: GeminiConstructionClient
) -> str:
    """
    Submits conversation messages to the Gemini chat client or heuristic engineering fallback.
    """
    return client.ask_engineering_assistant(
        messages=messages,
        system_context=ENGINEERING_ASSISTANT_SYSTEM_CONTEXT
    )
