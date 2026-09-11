from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping


@dataclass(frozen=True)
class ProfileSpec:
    code: str
    family: str
    stock_length_mm: int = 5800
    reinforcement_required_from_mm: int = 1200


@dataclass(frozen=True)
class GlassSpec:
    code: str
    thickness_mm: Decimal
    rate_per_sq_m: Decimal


@dataclass(frozen=True)
class HardwareSpec:
    code: str
    name: str
    unit_rate: Decimal


@dataclass(frozen=True)
class UPVCCatalog:
    profiles: Mapping[str, ProfileSpec]
    glass: Mapping[str, GlassSpec]
    hardware: Mapping[str, HardwareSpec]

    def profile(self, code: str) -> ProfileSpec:
        if code not in self.profiles:
            raise KeyError(f"Unknown profile system: {code}")
        return self.profiles[code]

    def glass_spec(self, code: str) -> GlassSpec:
        if code not in self.glass:
            raise KeyError(f"Unknown glass specification: {code}")
        return self.glass[code]

    def hardware_spec(self, code: str) -> HardwareSpec:
        if code not in self.hardware:
            raise KeyError(f"Unknown hardware specification: {code}")
        return self.hardware[code]
