from __future__ import annotations

from dataclasses import dataclass

from .models import UPVCConfiguration


@dataclass(frozen=True)
class EngineeringResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


class UPVCEngineeringAgent:
    """Deterministic engineering guardrail for configuration inputs.

    Manufacturer-specific limits must be injected as rules later; this first
    version only enforces generic dimensional and configuration invariants.
    """

    def validate(self, configuration: UPVCConfiguration) -> EngineeringResult:
        errors: list[str] = []
        warnings: list[str] = []
        measurement = configuration.opening.measurement

        if measurement.width_mm <= 0 or measurement.height_mm <= 0:
            errors.append("Opening dimensions must be positive")
        if measurement.width_mm < 300 or measurement.height_mm < 300:
            errors.append("Opening dimensions are below the minimum generic limit of 300 mm")
        if measurement.width_mm > 6000 or measurement.height_mm > 6000:
            errors.append("Opening dimensions exceed the generic 6000 mm limit")
        if configuration.sash_count < 1:
            errors.append("Sash count must be at least 1")
        if configuration.sash_count > 6:
            errors.append("Sash count exceeds the generic maximum of 6")
        if configuration.glass.value == "double" and min(measurement.width_mm, measurement.height_mm) < 400:
            warnings.append("Double glazing on a very small opening should be manually reviewed")
        if measurement.source not in {"manual", "site", "camera", "document"}:
            warnings.append(f"Unknown measurement source: {measurement.source}")

        return EngineeringResult(valid=not errors, errors=errors, warnings=warnings)
