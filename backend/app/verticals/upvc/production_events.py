from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ProductionStage(str, Enum):
    PLANNED = "planned"
    CUTTING = "cutting"
    REINFORCEMENT = "reinforcement"
    ASSEMBLY = "assembly"
    GLAZING = "glazing"
    QC = "qc"
    PACKING = "packing"
    DISPATCHED = "dispatched"
    COMPLETED = "completed"
    BLOCKED = "blocked"


_ALLOWED: dict[ProductionStage, set[ProductionStage]] = {
    ProductionStage.PLANNED: {ProductionStage.CUTTING, ProductionStage.BLOCKED},
    ProductionStage.CUTTING: {ProductionStage.REINFORCEMENT, ProductionStage.ASSEMBLY, ProductionStage.BLOCKED},
    ProductionStage.REINFORCEMENT: {ProductionStage.ASSEMBLY, ProductionStage.BLOCKED},
    ProductionStage.ASSEMBLY: {ProductionStage.GLAZING, ProductionStage.QC, ProductionStage.BLOCKED},
    ProductionStage.GLAZING: {ProductionStage.QC, ProductionStage.BLOCKED},
    ProductionStage.QC: {ProductionStage.PACKING, ProductionStage.ASSEMBLY, ProductionStage.BLOCKED},
    ProductionStage.PACKING: {ProductionStage.DISPATCHED, ProductionStage.BLOCKED},
    ProductionStage.DISPATCHED: {ProductionStage.COMPLETED, ProductionStage.BLOCKED},
    ProductionStage.COMPLETED: set(),
    ProductionStage.BLOCKED: {ProductionStage.PLANNED, ProductionStage.CUTTING, ProductionStage.REINFORCEMENT, ProductionStage.ASSEMBLY, ProductionStage.GLAZING, ProductionStage.QC},
}


@dataclass(frozen=True)
class ProductionEvent:
    order_id: str
    event_type: str
    stage: ProductionStage
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "system"
    confidence: float | None = None
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass
class ProductionState:
    order_id: str
    stage: ProductionStage = ProductionStage.PLANNED
    events: list[ProductionEvent] = field(default_factory=list)

    def transition(self, target: ProductionStage, *, source: str = "system", payload: dict[str, Any] | None = None) -> ProductionEvent:
        if target not in _ALLOWED[self.stage]:
            raise ValueError(f"Invalid production transition: {self.stage.value} -> {target.value}")
        event = ProductionEvent(
            order_id=self.order_id,
            event_type=f"production.{target.value}",
            stage=target,
            payload=payload or {},
            source=source,
        )
        self.stage = target
        self.events.append(event)
        return event

    def record_observation(
        self,
        event_type: str,
        *,
        source: str,
        payload: dict[str, Any] | None = None,
        confidence: float | None = None,
    ) -> ProductionEvent:
        event = ProductionEvent(
            order_id=self.order_id,
            event_type=event_type,
            stage=self.stage,
            payload=payload or {},
            source=source,
            confidence=confidence,
        )
        self.events.append(event)
        return event
