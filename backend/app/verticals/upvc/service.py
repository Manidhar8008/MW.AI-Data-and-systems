from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import uuid4

from .engineering import EngineeringResult, UPVCEngineeringAgent
from .estimation import BOM, Quote, UPVCEstimator
from .fabrication import ProductionOrder, UPVCFabricationPlanner
from .models import UPVCConfiguration


@dataclass(frozen=True)
class UPVCProductionBundle:
    engineering: EngineeringResult
    bom: BOM
    quote: Quote
    production_order: ProductionOrder


class UPVCProductionService:
    """Application service: one validated configuration produces one auditable bundle."""

    def __init__(
        self,
        engineering: UPVCEngineeringAgent | None = None,
        estimator: UPVCEstimator | None = None,
        fabrication: UPVCFabricationPlanner | None = None,
    ) -> None:
        self.engineering = engineering or UPVCEngineeringAgent()
        self.estimator = estimator or UPVCEstimator()
        self.fabrication = fabrication or UPVCFabricationPlanner()

    def build(self, configuration: UPVCConfiguration, order_id: str | None = None) -> UPVCProductionBundle:
        result = self.engineering.validate(configuration)
        if not result.valid:
            raise ValueError("Engineering validation failed: " + "; ".join(result.errors))
        bom = self.estimator.generate_bom(configuration)
        quote = self.estimator.quote(configuration)
        production_order = self.fabrication.plan(configuration, order_id or f"PO-{uuid4().hex[:10].upper()}")
        return UPVCProductionBundle(result, bom, quote, production_order)

    @staticmethod
    def summary(bundle: UPVCProductionBundle) -> dict[str, Any]:
        return {
            "engineering_valid": bundle.engineering.valid,
            "warnings": bundle.engineering.warnings,
            "quote": {
                "currency": bundle.quote.currency,
                "subtotal": str(bundle.quote.subtotal),
                "tax": str(bundle.quote.tax),
                "total": str(bundle.quote.total),
            },
            "production_order": {
                "id": bundle.production_order.order_id,
                "status": bundle.production_order.status,
                "profile_bars": len(bundle.production_order.profile_cuts.stocks),
                "profile_waste_mm": str(bundle.production_order.profile_cuts.waste_mm),
                "profile_utilization_percent": str(bundle.production_order.profile_cuts.utilization_percent),
                "reinforcement_bars": len(bundle.production_order.reinforcement_cuts.stocks),
            },
        }
