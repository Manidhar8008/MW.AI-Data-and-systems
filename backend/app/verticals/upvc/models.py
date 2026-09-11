from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class OpeningType(str, Enum):
    WINDOW = "window"
    DOOR = "door"


class GlassType(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"


@dataclass
class Measurement:
    width_mm: int
    height_mm: int
    sill_height_mm: int | None = None
    source: str = "manual"


@dataclass
class Opening:
    measurement: Measurement
    opening_type: OpeningType = OpeningType.WINDOW
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class UPVCConfiguration:
    opening: Opening
    glass: GlassType = GlassType.SINGLE
    finish: str = "white"
    profile_system: str = "standard"
    sash_count: int = 1
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "opening_id": self.opening.id,
            "opening_type": self.opening.opening_type.value,
            "width_mm": self.opening.measurement.width_mm,
            "height_mm": self.opening.measurement.height_mm,
            "sill_height_mm": self.opening.measurement.sill_height_mm,
            "measurement_source": self.opening.measurement.source,
            "glass": self.glass.value,
            "finish": self.finish,
            "profile_system": self.profile_system,
            "sash_count": self.sash_count,
        }
