from decimal import Decimal

import pytest

from app.verticals.upvc.onboarding import BusinessDocument, VerificationStatus
from app.verticals.upvc.onboarding_service import UPVCOnboardingService, UPVCOnboardingStore


def test_document_rate_is_pending_until_owner_verifies() -> None:
    service = UPVCOnboardingService()
    service_module_store = service_module_store_reset()
    document = BusinessDocument(name="rates.txt", document_type="rate_sheet")

    candidates = service.add_document("tenant-test", document, b"Default SFT Rate: Rs 650")

    assert candidates
    config = service.configuration("tenant-test")
    rule = config.rules["pricing.sft_rates.default"]
    assert rule.status is VerificationStatus.PENDING
    assert rule.source_document_id == document.id
    assert Decimal(str(rule.value["rate_per_sft"])) == Decimal("650")
    assert service.readiness(config)["ready_for_quotes"] is False
    assert service_module_store is not None


def test_verifying_sft_rule_unlocks_quote_readiness() -> None:
    service = UPVCOnboardingService()
    service.set_company_name("tenant-ready", "Example Fabricator")
    document = BusinessDocument(name="rates.txt", document_type="rate_sheet")
    service.add_document("tenant-ready", document, b"SFT Rate: 750")

    service.verify_rule("tenant-ready", "pricing.sft_rates.default")

    config = service.configuration("tenant-ready")
    assert config.rules["pricing.sft_rates.default"].status is VerificationStatus.VERIFIED
    assert service.readiness(config)["ready_for_quotes"] is True


def service_module_store_reset() -> UPVCOnboardingStore:
    """Return the backing store for an explicit contract check in this thin unit test."""
    return UPVCOnboardingStore()
