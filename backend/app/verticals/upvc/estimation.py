from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

from .engineering import EngineeringResult, UPVCEngineeringAgent
from .models import GlassType, UPVCConfiguration


MONEY_PLACES = Decimal("0.01")


@dataclass(frozen=True)
class PriceBook:
    profile_rate_per_meter: Decimal = Decimal("240")
    glass_rate_per_sq_meter_single: Decimal = Decimal("1400")
    glass_rate_per_sq_meter_double: Decimal = Decimal("2400")
    hardware_per_sash: Decimal = Decimal("450")
    hardware_per_door: Decimal = Decimal("850")
    wastage_percent: Decimal = Decimal("5")
    installation_percent: Decimal = Decimal("10")
    tax_percent: Decimal = Decimal("0")


@dataclass(frozen=True)
class BOMLineItem:
    category: str
    code: str
    description: str
    quantity: Decimal
    unit: str
    unit_rate: Decimal
    amount: Decimal


@dataclass(frozen=True)
class BOM:
    items: tuple[BOMLineItem, ...]
    subtotal: Decimal
    wastage: Decimal
    installation: Decimal
    total_before_tax: Decimal


@dataclass(frozen=True)
class QuoteLineItem:
    category: str
    description: str
    amount: Decimal


@dataclass(frozen=True)
class Quote:
    currency: str
    lines: tuple[QuoteLineItem, ...]
    subtotal: Decimal
    tax: Decimal
    total: Decimal


def money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def _profile_length_m(configuration: UPVCConfiguration) -> Decimal:
    m = configuration.opening.measurement
    perimeter_mm = Decimal(2 * (m.width_mm + m.height_mm))
    return perimeter_mm / Decimal(1000)


def _glass_area_sq_m(configuration: UPVCConfiguration) -> Decimal:
    m = configuration.opening.measurement
    return (Decimal(m.width_mm) * Decimal(m.height_mm)) / Decimal(1_000_000)


class UPVCEstimator:
    """Deterministic material estimator and BOM generator.

    All commercial rates are injected through PriceBook. No market prices are
    embedded in the domain. Replace the generic defaults with the fabricator's
    actual price book before using this for live customer quotations.
    """

    def __init__(self, price_book: PriceBook | None = None) -> None:
        self.price_book = price_book or PriceBook()
        self.engineering = UPVCEngineeringAgent()

    def generate_bom(self, configuration: UPVCConfiguration) -> BOM:
        engineering = self.engineering.validate(configuration)
        if not engineering.valid:
            raise ValueError("Engineering validation failed: " + "; ".join(engineering.errors))

        pb = self.price_book
        profile_qty = _profile_length_m(configuration)
        glass_qty = _glass_area_sq_m(configuration)
        glass_rate = (
            pb.glass_rate_per_sq_meter_double
            if configuration.glass is GlassType.DOUBLE
            else pb.glass_rate_per_sq_meter_single
        )
        hardware_rate = (
            pb.hardware_per_door
            if configuration.opening.opening_type.value == "door"
            else pb.hardware_per_sash
        )

        items = (
            self._line("profile", "UPVC-PROFILE", "uPVC profile perimeter", profile_qty, "m", pb.profile_rate_per_meter),
            self._line("glass", f"GLASS-{configuration.glass.value.upper()}", f"{configuration.glass.value} glazing", glass_qty, "m²", glass_rate),
            self._line("hardware", "HARDWARE-SET", "Hardware set", Decimal(configuration.sash_count), "set", hardware_rate),
        )
        subtotal = money(sum((item.amount for item in items), Decimal("0")))
        wastage = money(subtotal * pb.wastage_percent / Decimal("100"))
        installation = money((subtotal + wastage) * pb.installation_percent / Decimal("100"))
        total_before_tax = money(subtotal + wastage + installation)
        return BOM(items=items, subtotal=subtotal, wastage=wastage, installation=installation, total_before_tax=total_before_tax)

    @staticmethod
    def _line(category: str, code: str, description: str, quantity: Decimal, unit: str, unit_rate: Decimal) -> BOMLineItem:
        return BOMLineItem(
            category=category,
            code=code,
            description=description,
            quantity=quantity,
            unit=unit,
            unit_rate=money(unit_rate),
            amount=money(quantity * unit_rate),
        )

    def quote(self, configuration: UPVCConfiguration, currency: str = "INR") -> Quote:
        bom = self.generate_bom(configuration)
        pb = self.price_book
        lines = tuple(
            QuoteLineItem(item.category, item.description, item.amount) for item in bom.items
        ) + (
            QuoteLineItem("wastage", f"Wastage allowance ({pb.wastage_percent}%)", bom.wastage),
            QuoteLineItem("installation", f"Installation ({pb.installation_percent}%)", bom.installation),
        )
        subtotal = bom.total_before_tax
        tax = money(subtotal * pb.tax_percent / Decimal("100"))
        total = money(subtotal + tax)
        return Quote(currency=currency, lines=lines, subtotal=subtotal, tax=tax, total=total)


class UPVCProductionPipeline:
    """Single deterministic orchestration boundary for engineering → BOM → quote."""

    def __init__(self, estimator: UPVCEstimator | None = None) -> None:
        self.estimator = estimator or UPVCEstimator()
        self.engineering = self.estimator.engineering

    def run(self, configuration: UPVCConfiguration) -> tuple[EngineeringResult, BOM, Quote]:
        result = self.engineering.validate(configuration)
        if not result.valid:
            raise ValueError("Engineering validation failed: " + "; ".join(result.errors))
        bom = self.estimator.generate_bom(configuration)
        quote = self.estimator.quote(configuration)
        return result, bom, quote
