from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Iterable

from .engineering import UPVCEngineeringAgent
from .models import UPVCConfiguration

MM = Decimal("1")


def mm(value: int | Decimal) -> Decimal:
    return Decimal(value).quantize(MM, rounding=ROUND_HALF_UP)


class BOMCategory(str, Enum):
    PROFILE = "profile"
    GLASS = "glass"
    REINFORCEMENT = "reinforcement"
    HARDWARE = "hardware"


class CutMaterial(str, Enum):
    PROFILE = "profile"
    REINFORCEMENT = "reinforcement"


@dataclass(frozen=True)
class ProfileRule:
    code: str
    frame_allowance_mm: Decimal = Decimal("0")
    sash_allowance_mm: Decimal = Decimal("0")
    stock_length_mm: Decimal = Decimal("5800")


@dataclass(frozen=True)
class FabricationRules:
    profile: ProfileRule = ProfileRule(code="UPVC-FRAME-60")
    glass_clearance_mm: Decimal = Decimal("20")
    reinforcement_threshold_mm: Decimal = Decimal("1200")
    reinforcement_code: str = "REINF-STEEL"
    reinforcement_stock_length_mm: Decimal = Decimal("6000")
    hardware_code: str = "HW-STD"
    handle_per_sash: int = 1
    lock_per_sash: int = 1
    hinge_pairs_per_sash: int = 2
    saw_kerf_mm: Decimal = Decimal("3")


@dataclass(frozen=True)
class FabricationLineItem:
    category: BOMCategory
    code: str
    description: str
    quantity: Decimal
    unit: str


@dataclass(frozen=True)
class GlassPiece:
    code: str
    width_mm: Decimal
    height_mm: Decimal
    quantity: int


@dataclass(frozen=True)
class CutPiece:
    material: CutMaterial
    code: str
    length_mm: Decimal
    quantity: int
    source: str


@dataclass(frozen=True)
class StockCut:
    stock_length_mm: Decimal
    cuts_mm: tuple[Decimal, ...]
    offcut_mm: Decimal


@dataclass(frozen=True)
class CutPlan:
    material: CutMaterial
    stock_length_mm: Decimal
    kerf_mm: Decimal
    pieces: tuple[CutPiece, ...]
    stocks: tuple[StockCut, ...]
    total_piece_length_mm: Decimal
    total_stock_length_mm: Decimal
    total_kerf_mm: Decimal
    waste_mm: Decimal
    utilization_percent: Decimal


@dataclass(frozen=True)
class HardwareItem:
    code: str
    description: str
    quantity: int
    unit: str = "pcs"


@dataclass(frozen=True)
class ProductionOrder:
    order_id: str
    configuration_id: str
    status: str
    engineering_valid: bool
    fabrication_items: tuple[FabricationLineItem, ...]
    glass: tuple[GlassPiece, ...]
    reinforcement: tuple[CutPiece, ...]
    hardware: tuple[HardwareItem, ...]
    profile_cuts: CutPlan
    reinforcement_cuts: CutPlan
    warnings: tuple[str, ...]


class UPVCFabricationPlanner:
    """Turns a validated uPVC configuration into fabrication instructions."""

    def __init__(self, rules: FabricationRules | None = None) -> None:
        self.rules = rules or FabricationRules()
        self.engineering = UPVCEngineeringAgent()

    def build_profile_decomposition(self, configuration: UPVCConfiguration) -> list[CutPiece]:
        m = configuration.opening.measurement
        w, h = mm(m.width_mm), mm(m.height_mm)
        r = self.rules.profile
        pieces = [
            CutPiece(CutMaterial.PROFILE, r.code, w + r.frame_allowance_mm, 2, "outer_frame_width"),
            CutPiece(CutMaterial.PROFILE, r.code, h + r.frame_allowance_mm, 2, "outer_frame_height"),
        ]
        sash_width = w / Decimal(configuration.sash_count)
        for index in range(configuration.sash_count):
            pieces.extend([
                CutPiece(CutMaterial.PROFILE, f"{r.code}-SASH", sash_width + r.sash_allowance_mm, 2, f"sash_{index + 1}_width"),
                CutPiece(CutMaterial.PROFILE, f"{r.code}-SASH", h + r.sash_allowance_mm, 2, f"sash_{index + 1}_height"),
            ])
        return pieces

    def build_glass_dimensions(self, configuration: UPVCConfiguration) -> tuple[GlassPiece, ...]:
        m = configuration.opening.measurement
        sash_width = mm(m.width_mm) / Decimal(configuration.sash_count)
        glass_width = sash_width - self.rules.glass_clearance_mm
        glass_height = mm(m.height_mm) - self.rules.glass_clearance_mm
        if glass_width <= 0 or glass_height <= 0:
            raise ValueError("Calculated glass dimensions are not positive")
        return (GlassPiece(f"GLASS-{configuration.glass.value.upper()}", mm(glass_width), mm(glass_height), configuration.sash_count),)

    def build_reinforcement_schedule(self, configuration: UPVCConfiguration, profile_cuts: Iterable[CutPiece]) -> tuple[CutPiece, ...]:
        threshold = self.rules.reinforcement_threshold_mm
        output: list[CutPiece] = []
        for piece in profile_cuts:
            if piece.length_mm >= threshold:
                output.append(CutPiece(CutMaterial.REINFORCEMENT, self.rules.reinforcement_code, piece.length_mm, piece.quantity, f"reinforce:{piece.source}"))
        return tuple(output)

    def build_hardware_schedule(self, configuration: UPVCConfiguration) -> tuple[HardwareItem, ...]:
        n = configuration.sash_count
        return (
            HardwareItem("HANDLE", "Handle", self.rules.handle_per_sash * n),
            HardwareItem("LOCK", "Lock / espagnolette set", self.rules.lock_per_sash * n),
            HardwareItem("HINGE-PAIR", "Hinge pair", self.rules.hinge_pairs_per_sash * n),
        )

    def build_cut_plan(self, pieces: Iterable[CutPiece], stock_length_mm: Decimal, material: CutMaterial | None = None) -> CutPlan:
        expanded: list[CutPiece] = []
        for piece in pieces:
            expanded.extend(CutPiece(piece.material, piece.code, piece.length_mm, 1, piece.source) for _ in range(piece.quantity))
        expanded.sort(key=lambda item: item.length_mm, reverse=True)
        kerf = self.rules.saw_kerf_mm
        stocks: list[list[Decimal]] = []
        remaining: list[Decimal] = []
        for piece in expanded:
            required = piece.length_mm + kerf
            placed = False
            for index, rem in enumerate(remaining):
                if required <= rem:
                    stocks[index].append(piece.length_mm)
                    remaining[index] = rem - required
                    placed = True
                    break
            if not placed:
                stocks.append([piece.length_mm])
                remaining.append(stock_length_mm - required)
        stock_rows = tuple(StockCut(stock_length_mm, tuple(cuts), remaining[index]) for index, cuts in enumerate(stocks))
        piece_length = sum((item.length_mm for item in expanded), Decimal("0"))
        total_kerf = kerf * Decimal(len(expanded))
        total_stock = stock_length_mm * Decimal(len(stock_rows))
        waste = total_stock - piece_length - total_kerf
        utilization = ((piece_length + total_kerf) / total_stock * Decimal("100")) if total_stock else Decimal("0")
        return CutPlan(material or (expanded[0].material if expanded else CutMaterial.PROFILE), stock_length_mm, kerf, tuple(expanded), stock_rows, mm(piece_length), mm(total_stock), mm(total_kerf), mm(waste), utilization.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    def plan(self, configuration: UPVCConfiguration, order_id: str) -> ProductionOrder:
        engineering = self.engineering.validate(configuration)
        if not engineering.valid:
            raise ValueError("Engineering validation failed: " + "; ".join(engineering.errors))
        profile_cuts = self.build_profile_decomposition(configuration)
        glass = self.build_glass_dimensions(configuration)
        reinforcement = self.build_reinforcement_schedule(configuration, profile_cuts)
        hardware = self.build_hardware_schedule(configuration)
        return ProductionOrder(
            order_id=order_id,
            configuration_id=configuration.id,
            status="ready_for_production",
            engineering_valid=True,
            fabrication_items=(
                FabricationLineItem(BOMCategory.PROFILE, self.rules.profile.code, "uPVC profile stock", Decimal(sum(p.quantity for p in profile_cuts)), "pcs"),
                FabricationLineItem(BOMCategory.GLASS, glass[0].code, "Glazing panels", Decimal(sum(g.quantity for g in glass)), "pcs"),
                FabricationLineItem(BOMCategory.REINFORCEMENT, self.rules.reinforcement_code, "Steel reinforcement pieces", Decimal(sum(p.quantity for p in reinforcement)), "pcs"),
                FabricationLineItem(BOMCategory.HARDWARE, self.rules.hardware_code, "Hardware schedule", Decimal(sum(h.quantity for h in hardware)), "pcs"),
            ),
            glass=glass,
            reinforcement=reinforcement,
            hardware=hardware,
            profile_cuts=self.build_cut_plan(profile_cuts, self.rules.profile.stock_length_mm, CutMaterial.PROFILE),
            reinforcement_cuts=self.build_cut_plan(reinforcement, self.rules.reinforcement_stock_length_mm, CutMaterial.REINFORCEMENT),
            warnings=tuple(engineering.warnings),
        )
