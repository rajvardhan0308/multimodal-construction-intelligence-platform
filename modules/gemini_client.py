"""
Gemini Multimodal Client & Graceful Demonstration Fallback Engine
Platform ID: 6ac4c98d1dcde6d7857c1642
"""

import os
import json
import re
import warnings
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image

warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

from config import DEFAULT_VISION_MODEL, DEFAULT_CHAT_MODEL


class GeminiConstructionClient:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the Gemini Multimodal client.
        If no API key is provided, system operates in standalone Demonstration Mode.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.is_configured = False
        self.client_error = None
        self._init_client()

    def _init_client(self):
        if not HAS_GENAI:
            self.client_error = "google-generativeai package not installed."
            self.is_configured = False
            return

        if self.api_key and len(self.api_key) > 8:
            try:
                genai.configure(api_key=self.api_key)
                self.is_configured = True
                self.client_error = None
            except Exception as e:
                self.is_configured = False
                self.client_error = str(e)
        else:
            self.is_configured = False

    def is_demo_mode(self) -> bool:
        """Returns True if operating in Demonstration fallback mode."""
        return not self.is_configured

    @staticmethod
    def clean_json_response(raw_text: str) -> Dict[str, Any]:
        """
        Sanitizes and extracts pure JSON from LLM multimodal output.
        Handles markdown backticks (```json ... ```) and loose formatting.
        """
        cleaned = raw_text.strip()
        # Remove markdown code fence if present
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
            cleaned = re.sub(r"\n?```$", "", cleaned)
            cleaned = cleaned.strip()

        # Find first '{' and last '}'
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx >= start_idx:
            cleaned = cleaned[start_idx:end_idx + 1]

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as err:
            # Fallback regex or error dictionary
            return {
                "error": "Failed to parse JSON response",
                "raw_preview": raw_text[:500],
                "details": str(err)
            }

    def analyze_image_multimodal(
        self,
        image: Image.Image,
        prompt: str,
        system_instruction: Optional[str] = None,
        model_name: str = DEFAULT_VISION_MODEL
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Submits image + prompt to Gemini Vision.
        Returns (parsed_json, error_message).
        """
        if self.is_demo_mode():
            return None, "Demo mode active (no live API key)."

        try:
            generation_config = {
                "temperature": 0.2,
                "top_p": 0.95,
                "response_mime_type": "application/json"
            }
            kwargs = {}
            if system_instruction:
                kwargs["system_instruction"] = system_instruction

            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                **kwargs
            )
            response = model.generate_content([prompt, image])
            if response and response.text:
                parsed = self.clean_json_response(response.text)
                return parsed, None
            else:
                return None, "Empty response from multimodal model."
        except Exception as e:
            # Fallback attempt without response_mime_type in case of model version restriction
            try:
                model = genai.GenerativeModel(model_name=model_name)
                response = model.generate_content([prompt, image])
                if response and response.text:
                    parsed = self.clean_json_response(response.text)
                    return parsed, None
            except Exception as e2:
                err_msg = str(e2)
                return None, f"Gemini API Exception: {err_msg}"
            return None, f"Gemini API Exception: {str(e)}"

    def ask_engineering_assistant(
        self,
        messages: List[Dict[str, str]],
        system_context: str,
        model_name: str = DEFAULT_CHAT_MODEL
    ) -> str:
        """
        Multi-turn chat completion for Construction Engineering Assistant.
        """
        if self.is_demo_mode():
            # Return intelligent simulated engineering response
            last_msg = messages[-1]["content"] if messages else ""
            return self._generate_simulated_chat_response(last_msg)

        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_context
            )
            # Format history for chat
            gemini_history = []
            for m in messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [m["content"]]})

            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(messages[-1]["content"])
            return response.text if response and response.text else "No response generated."
        except Exception as e:
            return f"⚠️ Chat service error: {str(e)}. (Tip: Verify API key or continue in Demo Mode)."

    def _generate_simulated_chat_response(self, user_prompt: str) -> str:
        """Domain-grounded heuristic response for offline demonstration."""
        prompt_lower = user_prompt.lower()
        if "curing" in prompt_lower or "is 456" in prompt_lower or "opc" in prompt_lower:
            return (
                "**Chartered Engineering Advisory [IS 456:2000 Clause 13.5 Standards]:**\n\n"
                "1. **Ordinary Portland Cement (OPC 43/53):**\n"
                "   - Under standard ambient conditions: **Minimum 7 days** continuous moist curing.\n"
                "   - Under dry/hot weather conditions (ambient temp > 35°C, humidity < 50%): **Minimum 10 days**.\n\n"
                "2. **Mineral Admixtures / Blended Cement (PPC / PSC / Fly Ash / GGBS):**\n"
                "   - Hydration reaction of pozzolanic materials is significantly slower.\n"
                "   - **Minimum 10 days** moist curing is mandatory under normal weather, extending to **14 days** in hot/arid climates.\n\n"
                "3. **Practical Quality Rule:** Premature cessation of water ponding leads to superficial micro-crazing and up to 30% loss of compressive strength at 28 days."
            )
        elif "crack" in prompt_lower or "permissible" in prompt_lower or "width" in prompt_lower:
            return (
                "**Structural Defect Tolerances [IS 456:2000 Cl. 35.3.2 & BS 8110]:**\n\n"
                "- **Mild Exposure (Indoor dry elements):** Permissible crack width limit is **0.30 mm**.\n"
                "- **Moderate Exposure (Sheltered exterior / foundation above water table):** Max limit is **0.20 mm**.\n"
                "- **Severe / Very Severe / Marine Exposure (Splash zone, industrial coastal):** Strict limit of **0.10 mm** to prevent chloride-induced rebar depassivation.\n\n"
                "**Immediate Action Protocol:** Any shear crack propagating at 45° across beam-column nodes exceeding 0.25 mm requires structural shoring followed by low-viscosity epoxy pressure injection."
            )
        elif "fall" in prompt_lower or "osha" in prompt_lower or "scaffold" in prompt_lower or "height" in prompt_lower:
            return (
                "**OSHA 1926 Subpart M & IS 3696 Fall Protection Framework:**\n\n"
                "- **Trigger Height:** OSHA 1926.501 requires fall protection at **6 feet (1.8 meters)** above a lower level; for supported scaffoldings (1926.451), guardrails are mandatory above **10 feet (3.1 meters)**.\n"
                "- **Guardrail Geometry:** Top rail at **42 inches ± 3 inches (107 cm)** capable of withstanding a 200 lb outward load; midrail at **21 inches (53 cm)**; toeboard height minimum **3.5 inches (9 cm)**.\n"
                "- **Harness Anchoring (IS 3521):** Full-body harnesses must be tethered to engineered anchor points certified for **5,000 lbs (22.2 kN)** per worker with deceleration lanyards limiting arresting force to < 8 kN."
            )
        elif "wind" in prompt_lower or "crane" in prompt_lower or "speed" in prompt_lower:
            return (
                "**IS 875 (Part 3) & OSHA 1926.1431 High Wind Lift Protocol:**\n\n"
                "- **Threshold Limit:** Tower cranes must cease lifting operations when sustained wind speeds exceed **38 km/h (approx. 20 knots / 10.5 m/s)** or wind gusts reach 45 km/h.\n"
                "- **Storm Parking:** Disengage slew brake to leave the jib in 'weathervane' condition (allows crane head to rotate naturally with wind direction without torsional lattice buckling).\n"
                "- **Man-Baskets:** Personnel platform lifts must be aborted if winds exceed **32 km/h (20 mph)**."
            )
        else:
            return (
                f"**Senior Structural Engineering Review:**\n\n"
                f"Analyzing technical query: *\"{user_prompt}\"*\n\n"
                "According to standard CPWD Technical Specifications and IS 456 / OSHA regulations:\n"
                "1. **Safety First:** Maintain zero-tolerance for un-shored trenches, missing edge guardrails, and non-certified lifting tackle.\n"
                "2. **Quality Assurance:** Ensure 7-day cube testing (target > 67% fck) and 28-day compliance (target ≥ fck + 1.65σ) for all structural concrete pours.\n"
                "3. **Documentation:** Log daily weather parameters, slump test results, batching tickets, and pour sign-offs in the Site QA/QC Register."
            )
