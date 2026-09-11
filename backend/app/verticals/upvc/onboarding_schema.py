from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OnboardingField:
    key: str
    label: str
    category: str
    required: bool = True
    affects_money: bool = False
    affects_production: bool = False


ONBOARDING_FIELDS = (
    OnboardingField("company.name", "Company name", "company"),
    OnboardingField("company.phone", "Company phone", "company"),
    OnboardingField("products.supported", "Supported products", "products"),
    OnboardingField("profiles.systems", "Profile systems / brands", "profiles", affects_production=True),
    OnboardingField("pricing.sft_rates", "SFT rates", "pricing", affects_money=True),
    OnboardingField("pricing.glass_rates", "Glass rates", "pricing", affects_money=True),
    OnboardingField("pricing.hardware_rates", "Hardware rates", "pricing", affects_money=True),
    OnboardingField("pricing.installation", "Installation pricing", "pricing", affects_money=True),
    OnboardingField("pricing.transport", "Transport pricing", "pricing", affects_money=True),
    OnboardingField("pricing.tax", "Tax rules", "pricing", affects_money=True),
    OnboardingField("engineering.rules", "Fabrication / engineering rules", "engineering", affects_production=True),
    OnboardingField("production.workflow", "Workshop workflow", "production", affects_production=True),
    OnboardingField("production.stock_lengths", "Stock lengths", "production", affects_production=True),
    OnboardingField("qc.checklist", "QC checklist", "quality", affects_production=True),
    OnboardingField("communication.channels", "Communication channels", "communication"),
)

DOCUMENT_TYPES = (
    "rate_sheet",
    "profile_catalogue",
    "price_list",
    "price_book",
    "quotation_example",
    "bom_example",
    "cutting_list",
    "measurement_sheet",
    "sop",
    "qc_checklist",
    "supplier_list",
    "product_catalogue",
    "other",
)
