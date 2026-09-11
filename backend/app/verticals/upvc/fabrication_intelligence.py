from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .production_events import ProductionEvent


@dataclass(frozen=True)
class ProductionObservation:
    event_type: str
    payload: dict[str, Any]
    confidence: float = 1.0
    source: str = "camera"


@dataclass(frozen=True)
class ReconciliationResult:
    matched: bool
    anomalies: tuple[str, ...]
    expected_event_types: tuple[str, ...]
    observed_event_types: tuple[str, ...]


class FabricationIntelligence:
    """Deterministic reconciliation layer for future camera/machine observations."""

    def reconcile(
        self,
        expected_events: Iterable[str],
        observed_events: Iterable[ProductionEvent | ProductionObservation],
    ) -> ReconciliationResult:
        expected = tuple(expected_events)
        observed = tuple(item.event_type for item in observed_events)
        anomalies: list[str] = []

        expected_set = set(expected)
        observed_set = set(observed)
        for missing in sorted(expected_set - observed_set):
            anomalies.append(f"Expected event not observed: {missing}")

        unexpected = sorted(observed_set - expected_set)
        for extra in unexpected:
            anomalies.append(f"Observed event not in plan: {extra}")

        return ReconciliationResult(
            matched=not anomalies,
            anomalies=tuple(anomalies),
            expected_event_types=expected,
            observed_event_types=observed,
        )
