from __future__ import annotations

from .models import GlassType, Measurement, Opening, OpeningType, UPVCConfiguration
from .pipeline import UPVCProductionPipeline


def main() -> None:
    configuration = UPVCConfiguration(
        opening=Opening(
            measurement=Measurement(width_mm=1200, height_mm=1500, source="site"),
            opening_type=OpeningType.WINDOW,
        ),
        glass=GlassType.DOUBLE,
        finish="white",
        profile_system="standard",
        sash_count=2,
    )

    result = UPVCProductionPipeline().run(configuration, order_id="PO-DEMO-001")

    print("ENGINEERING VALID:", result.engineering.valid)
    print("BOM:")
    for item in result.bom.items:
        print(f"  {item.code}: {item.quantity} {item.unit} × ₹{item.unit_rate} = ₹{item.amount}")
    print("QUOTE TOTAL:", result.quote.total)
    print("GLASS:")
    for piece in result.production_order.glass:
        print(f"  {piece.code}: {piece.quantity} × {piece.width_mm} × {piece.height_mm} mm")
    print("PROFILE CUTS:")
    for stock in result.production_order.profile_cuts.stocks:
        print(f"  {stock.cuts_mm} | offcut={stock.offcut_mm} mm")
    print("HARDWARE:")
    for item in result.production_order.hardware:
        print(f"  {item.description}: {item.quantity} {item.unit}")
    print("PRODUCTION STATUS:", result.production_order.status)


if __name__ == "__main__":
    main()
