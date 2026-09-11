from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import json
import re
from typing import Any

from .onboarding import (
    BusinessDocument,
    ConfigurationRule,
    FabricatorConfiguration,
    RuleSource,
    VerificationStatus,
)


@dataclass(frozen=True)
class ExtractedRule:
    key: str
    value: Any
    confidence: Decimal
    source_document_id: str
    evidence: str
    affects_money: bool = False
    affects_production: bool = False


class UPVCOnboardingStore:
    """Process-local onboarding store for the first API slice.

    The contract is intentionally repository-shaped so it can be replaced by
    SQLAlchemy without changing the API semantics. Production persistence must
    move this store to the application database before multi-instance deployment.
    """

    def __init__(self) -> None:
        self._configurations: dict[str, FabricatorConfiguration] = {}

    def get_or_create(self, tenant_id: str, company_name: str = "") -> FabricatorConfiguration:
        config = self._configurations.get(tenant_id)
        if config is None:
            config = FabricatorConfiguration(tenant_id=tenant_id, company_name=company_name.strip())
            self._configurations[tenant_id] = config
        elif company_name.strip() and not config.company_name:
            config.company_name = company_name.strip()
        return config


store = UPVCOnboardingStore()


class UPVCDocumentExtractor:
    """Safe first-pass extractor; AI providers can implement the same contract later."""

    _RATE_PATTERNS = (
        re.compile(r"(?i)(?:rate|price)\s*(?:/|per)?\s*sft\s*[:=-]\s*₹?\s*([0-9]+(?:\.[0-9]+)?)"),
        re.compile(r"(?i)sft\s*(?:rate|price)\s*[:=-]\s*₹?\s*([0-9]+(?:\.[0-9]+)?)"),
    )

    def extract(self, document: BusinessDocument, content: bytes) -> list[ExtractedRule]:
        text = self._decode_text(content)
        if not text:
            return []

        extracted: list[ExtractedRule] = []
        for pattern in self._RATE_PATTERNS:
            match = pattern.search(text)
            if match:
                extracted.append(
                    ExtractedRule(
                        key="pricing.sft_rates.default",
                        value={"rate_per_sft": str(Decimal(match.group(1)))},
                        confidence=Decimal("0.72"),
                        source_document_id=document.id,
                        evidence=match.group(0),
                        affects_money=True,
                    )
                )
                break

        try:
            payload = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            payload = None

        if isinstance(payload, dict):
            for key, value in payload.items():
                normalized = str(key).strip()
                if normalized in {"company.name", "company.phone", "products.supported", "profiles.systems"}:
                    extracted.append(
                        ExtractedRule(
                            key=normalized,
                            value=value,
                            confidence=Decimal("0.90"),
                            source_document_id=document.id,
                            evidence=f"JSON field: {normalized}",
                            affects_production=normalized == "profiles.systems",
                        )
                    )

        return self._deduplicate(extracted)

    @staticmethod
    def _decode_text(content: bytes) -> str:
        if not content:
            return ""
        for encoding in ("utf-8", "utf-8-sig"):
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                continue
        return ""

    @staticmethod
    def _deduplicate(items: list[ExtractedRule]) -> list[ExtractedRule]:
        by_key: dict[str, ExtractedRule] = {}
        for item in items:
            existing = by_key.get(item.key)
            if existing is None or item.confidence > existing.confidence:
                by_key[item.key] = item
        return list(by_key.values())


class UPVCOnboardingService:
    def __init__(self, extractor: UPVCDocumentExtractor | None = None) -> None:
        self.extractor = extractor or UPVCDocumentExtractor()

    def configuration(self, tenant_id: str, company_name: str = "") -> FabricatorConfiguration:
        return store.get_or_create(tenant_id, company_name)

    def add_document(
        self,
        tenant_id: str,
        document: BusinessDocument,
        content: bytes,
    ) -> list[ExtractedRule]:
        config = self.configuration(tenant_id)
        config.add_document(document)
        for candidate in self.extractor.extract(document, content):
            config.add_rule(
                ConfigurationRule(
                    key=candidate.key,
                    value=candidate.value,
                    source=RuleSource.DOCUMENT,
                    confidence=candidate.confidence,
                    status=VerificationStatus.PENDING,
                    source_document_id=candidate.source_document_id,
                )
            )
        return self.extractor.extract(document, content)

    def set_company_name(self, tenant_id: str, company_name: str) -> FabricatorConfiguration:
        config = self.configuration(tenant_id)
        config.company_name = company_name.strip()
        config.add_rule(
            ConfigurationRule(
                key="company.name",
                value=config.company_name,
                source=RuleSource.OWNER,
                confidence=Decimal("1.00"),
                status=VerificationStatus.VERIFIED,
            )
        )
        return config

    def verify_rule(self, tenant_id: str, key: str) -> ConfigurationRule:
        config = self.configuration(tenant_id)
        rule = config.rules.get(key)
        if rule is None:
            raise KeyError(f"Unknown onboarding rule: {key}")
        updated = ConfigurationRule(
            key=rule.key,
            value=rule.value,
            source=rule.source,
            confidence=rule.confidence,
            status=VerificationStatus.VERIFIED,
            source_document_id=rule.source_document_id,
        )
        config.add_rule(updated)
        return updated

    def reject_rule(self, tenant_id: str, key: str) -> ConfigurationRule:
        config = self.configuration(tenant_id)
        rule = config.rules.get(key)
        if rule is None:
            raise KeyError(f"Unknown onboarding rule: {key}")
        updated = ConfigurationRule(
            key=rule.key,
            value=rule.value,
            source=rule.source,
            confidence=rule.confidence,
            status=VerificationStatus.REJECTED,
            source_document_id=rule.source_document_id,
        )
        config.add_rule(updated)
        return updated

    @staticmethod
    def readiness(config: FabricatorConfiguration) -> dict[str, Any]:
        pending_money = []
        pending_production = []
        for key, rule in config.rules.items():
            if rule.status is not VerificationStatus.VERIFIED:
                if key.startswith("pricing."):
                    pending_money.append(key)
                if key.startswith(("profiles.", "engineering.", "production.")):
                    pending_production.append(key)

        return {
            "tenant_id": config.tenant_id,
            "company_name": config.company_name,
            "document_count": len(config.documents),
            "rule_count": len(config.rules),
            "verified_rule_count": len(config.verified_rules()),
            "pending_money_rules": sorted(pending_money),
            "pending_production_rules": sorted(pending_production),
            "ready_for_quotes": bool(config.company_name) and not pending_money and any(
                key.startswith("pricing.sft_rates") for key in config.verified_rules()
            ),
            "ready_for_production": bool(config.company_name) and not pending_production,
        }
