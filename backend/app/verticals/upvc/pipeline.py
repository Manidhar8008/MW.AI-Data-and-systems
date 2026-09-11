from __future__ import annotations

from dataclasses import dataclass

from .engineering import EngineeringResult, UPVCEngineeringAgent
from .estimation import BOM, Quote, UPVCEstimator
from .fabrication import ProductionOrder, UPVCFabricationPlanner
from .models import UPVCConfiguration


@dataclass(frozen=True)
class UPVCProductionResult:
    engineering: EngineeringResult
    bom: BOM
    quote: Quote
    production_order: ProductionOrder


class UPVCProductionPipeline:
    """Deterministic boundary from configuration to factory-ready instructions."""

    def __init__(
        self,
        estimator: UPVCEstimator | None = None,
        fabrication: UPVCFabricationPlanner | None = None,
    ) -> None:
        self.estimator = estimator or UPVCEstimator()
        self.engineering = self.estimator.engineering
        self.fabrication = fabrication or UPVCFabricationPlanner()

    def run(self, configuration: UPVCConfiguration, order_id: str = "PO-DRAFT") -> UPVCProductionResult:
        engineering = self.engineering.validate(configuration)
        if not engineering.valid:
            raise ValueError("Engineering validation failed: " + "; ".join(engineering.errors))

        bom = self.estimator.generate_bom(configuration)
        quote = self.estimator.quote(configuration)
        production_order = self.fabrication.plan(configuration, order_id)
        return UPVCProductionResult(
            engineering=engineering,
            bom=bom,
            quote=quote,
            production_order=production_order,
        )
