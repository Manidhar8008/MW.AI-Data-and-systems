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
    INSTALLED = "installed"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


_ALLOWED: dict[ProductionStage, set[ProductionStage]] = {
    ProductionStage.PLANNED: {ProductionStage.CUTTING, ProductionStage.ON_HOLD},
    ProductionStage.CUTTING: {ProductionStage.REINFORCEMENT, ProductionStage.ON_HOLD},
    ProductionStage.REINFORCEMENT: {ProductionStage.ASSEMBLY, ProductionStage.ON_HOLD},
    ProductionStage.ASSEMBLY: {ProductionStage.GLAZING, ProductionStage.QC, ProductionStage.ON_HOLD},
    ProductionStage.GLAZING: {ProductionStage.QC, ProductionStage.ON_HOLD},
    ProductionStage.QC: {ProductionStage.PACKING, ProductionStage.ON_HOLD},
    ProductionStage.PACKING: {ProductionStage.DISPATCHED, ProductionStage.ON_HOLD},
    ProductionStage.DISPATCHED: {ProductionStage.INSTALLED, ProductionStage.ON_HOLD},
    ProductionStage.INSTALLED: {ProductionStage.COMPLETED, ProductionStage.ON_HOLD},
    ProductionStage.COMPLETED: set(),
    ProductionStage.ON_HOLD: set(ProductionStage),
}


@dataclass(frozen=True)
class ProductionEvent:
    production_order_id: str
    event_type: str
    stage: ProductionStage
    source: str
    payload: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if not self.production_order_id or not self.event_type or not self.source:
            raise ValueError("production_order_id, event_type and source are required")


@dataclass
class ProductionState:
    production_order_id: str
    stage: ProductionStage = ProductionStage.PLANNED
    events: list[ProductionEvent] = field(default_factory=list)

    def transition(self, target: ProductionStage, *, source: str = "system", reason: str | None = None) -> ProductionEvent:
        if target not in _ALLOWED[self.stage]:
            raise ValueError(f"Invalid production transition: {self.stage.value} -> {target.value}")
        previous = self.stage
        self.stage = target
        event = ProductionEvent(
            production_order_id=self.production_order_id,
            event_type="production.stage_changed",
            stage=target,
            source=source,
            payload={"from": previous.value, "to": target.value, "reason": reason},
        )
        self.events.append(event)
        return event

    def record_observation(self, event_type: str, *, source: str, payload: dict[str, Any], confidence: float = 1.0) -> ProductionEvent:
        event = ProductionEvent(
            production_order_id=self.production_order_id,
            event_type=event_type,
            stage=self.stage,
            source=source,
            payload=payload,
            confidence=confidence,
        )
        self.events.append(event)
        return event


@dataclass(frozen=True)
class ReconciliationResult:
    matched: bool
    score: float
    missing: tuple[str, ...] = ()
    unexpected: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


def reconcile_expected_events(expected: list[str], observed: list[str]) -> ReconciliationResult:
    expected_counts: dict[str, int] = {}
    observed_counts: dict[str, int] = {}
    for value in expected:
        expected_counts[value] = expected_counts.get(value, 0) + 1
    for value in observed:
        observed_counts[value] = observed_counts.get(value, 0) + 1
    missing: list[str] = []
    unexpected: list[str] = []
    for key, count in expected_counts.items():
        missing.extend([key] * max(0, count - observed_counts.get(key, 0)))
    for key, count in observed_counts.items():
        unexpected.extend([key] * max(0, count - expected_counts.get(key, 0)))
    total = max(len(expected), len(observed), 1)
    score = max(0.0, 1.0 - (len(missing) + len(unexpected)) / total)
    return ReconciliationResult(not missing and not unexpected, score, tuple(missing), tuple(unexpected))
