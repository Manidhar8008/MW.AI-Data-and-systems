from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class UPVCFabricationRules:
    """System-specific fabrication constants.

    These defaults are engineering placeholders. A live installation must load
    the actual profile manufacturer's dimensions, clearances and reinforcement
    requirements into tenant-scoped configuration.
    """

    frame_profile_code: str = "FRAME"
    sash_profile_code: str = "SASH"
    reinforcement_code: str = "STEEL-REINF"
    glazing_bead_code: str = "GLAZING-BEAD"
    frame_mitre_allowance_mm: int = 0
    sash_mitre_allowance_mm: int = 0
    glass_clearance_mm: int = 5
    bead_clearance_mm: int = 2
    reinforcement_threshold_mm: int = 1200
    reinforcement_clearance_mm: int = 20
    saw_kerf_mm: Decimal = Decimal("3")
    stock_bar_length_mm: int = 5800
    max_stock_bars: int = 100
