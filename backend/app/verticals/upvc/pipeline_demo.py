from __future__ import annotations

from decimal import Decimal

from .estimation import PriceBook, UPVCProductionPipeline
from .models import GlassType, Measurement, Opening, OpeningType, UPVCConfiguration


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

    pipeline = UPVCProductionPipeline(
        UPVCProductionPipeline.__annotations__ and None
    )
    engineering, bom, quote = pipeline.run(configuration)

    print("ENGINEERING:", engineering)
    print("BOM:")
    for item in bom.items:
        print(f"  {item.code}: {item.quantity} {item.unit} × ₹{item.unit_rate} = ₹{item.amount}")
    print("SUBTOTAL:", quote.subtotal)
    print("TAX:", quote.tax)
    print("TOTAL:", quote.total)


if __name__ == "__main__":
    main()
