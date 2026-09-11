from decimal import Decimal

from .fabrication import CutMaterial, UPVCFabricationPlanner
from .models import GlassType, Measurement, Opening, OpeningType, UPVCConfiguration
from .pipeline import UPVCProductionPipeline


def make_configuration() -> UPVCConfiguration:
    return UPVCConfiguration(
        opening=Opening(
            measurement=Measurement(width_mm=1200, height_mm=1500, source="site"),
            opening_type=OpeningType.WINDOW,
        ),
        glass=GlassType.DOUBLE,
        sash_count=2,
    )


def test_profile_decomposition_has_frame_and_sash_members() -> None:
    pieces = UPVCFabricationPlanner().build_profile_decomposition(make_configuration())
    assert len(pieces) == 6
    assert sum(piece.quantity for piece in pieces) == 12
    assert all(piece.material is CutMaterial.PROFILE for piece in pieces)


def test_glass_dimensions_are_positive() -> None:
    glass = UPVCFabricationPlanner().build_glass_dimensions(make_configuration())
    assert glass[0].quantity == 2
    assert glass[0].width_mm == Decimal("580")
    assert glass[0].height_mm == Decimal("1480")


def test_pipeline_produces_quote_and_ready_order() -> None:
    result = UPVCProductionPipeline().run(make_configuration(), order_id="PO-TEST-001")
    assert result.engineering.valid is True
    assert result.quote.total > 0
    assert result.production_order.order_id == "PO-TEST-001"
    assert result.production_order.status == "ready_for_production"
    assert len(result.production_order.profile_cuts.stocks) > 0
