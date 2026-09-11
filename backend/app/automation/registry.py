from __future__ import annotations

from typing import Any

from .engine import AutomationEngine
from .models import AutomationDefinition


def _normalize_upvc_enquiry(data: dict[str, Any]) -> dict[str, Any]:
    required = ("customer_name", "phone", "width_mm", "height_mm")
    missing = [key for key in required if data.get(key) in (None, "")]
    if missing:
        raise ValueError(f"Missing required enquiry fields: {', '.join(missing)}")

    width = float(data["width_mm"])
    height = float(data["height_mm"])
    if width <= 0 or height <= 0:
        raise ValueError("Opening dimensions must be positive")

    return {
        "customer_name": str(data["customer_name"]).strip(),
        "phone": str(data["phone"]).strip(),
        "width_mm": width,
        "height_mm": height,
        "glass": data.get("glass", "single"),
        "finish": data.get("finish", "white"),
        "status": "qualified",
    }


def _verify_normalized(_: dict[str, Any], output: dict[str, Any]) -> bool:
    return output.get("status") == "qualified" and output.get("width_mm", 0) > 0 and output.get("height_mm", 0) > 0


def build_default_engine() -> AutomationEngine:
    engine = AutomationEngine()
    engine.register(
        AutomationDefinition(
            id="upvc.normalize_enquiry",
            vertical="upvc",
            name="Normalize uPVC enquiry",
            classification="AUTOMATE",
            trigger_event="upvc.enquiry.created",
            action=_normalize_upvc_enquiry,
            verify=_verify_normalized,
            metadata={"stage": "intake", "next": "upvc.engineer.validate_opening"},
        )
    )
    return engine
