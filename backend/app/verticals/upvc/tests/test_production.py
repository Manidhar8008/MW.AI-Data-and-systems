import pytest

from app.verticals.upvc.production import (
    ProductionStage,
    ProductionState,
    reconcile_expected_events,
)


def test_valid_production_transition_and_event() -> None:
    state = ProductionState("PO-1")
    event = state.transition(ProductionStage.CUTTING, source="operator")
    assert state.stage is ProductionStage.CUTTING
    assert event.payload["from"] == "planned"


def test_invalid_production_transition_is_rejected() -> None:
    state = ProductionState("PO-1")
    with pytest.raises(ValueError):
        state.transition(ProductionStage.GLAZING)


def test_reconciliation_detects_missing_and_unexpected_events() -> None:
    result = reconcile_expected_events(
        ["cut.completed", "cut.completed", "glass.received"],
        ["cut.completed", "unexpected.event"],
    )
    assert not result.matched
    assert result.missing == ("cut.completed", "glass.received")
    assert result.unexpected == ("unexpected.event",)
    assert result.score < 1
