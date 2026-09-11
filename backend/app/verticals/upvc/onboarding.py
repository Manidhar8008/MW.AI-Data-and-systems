from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import uuid4


class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class RuleSource(str, Enum):
    OWNER = "owner"
    DOCUMENT = "document"
    AI_INFERRED = "ai_inferred"


@dataclass(frozen=True)
class BusinessDocument:
    name: str
    document_type: str
    source_uri: str | None = None
    id: str = field(default_factory=lambda: f"DOC-{uuid4().hex[:10].upper()}")


@dataclass(frozen=True)
class ConfigurationRule:
    key: str
    value: Any
    source: RuleSource
    confidence: Decimal = Decimal("1.00")
    status: VerificationStatus = VerificationStatus.PENDING
    source_document_id: str | None = None

    def __post_init__(self) -> None:
        if not Decimal("0") <= self.confidence <= Decimal("1"):
            raise ValueError("confidence must be between 0 and 1")


@dataclass
class FabricatorConfiguration:
    """Tenant-specific uPVC business configuration.

    Generic MW.AI code must not silently replace these rules. Money- or
    production-affecting rules should be verified by the fabricator before use.
    """

    tenant_id: str
    company_name: str
    documents: list[BusinessDocument] = field(default_factory=list)
    rules: dict[str, ConfigurationRule] = field(default_factory=dict)

    def add_document(self, document: BusinessDocument) -> None:
        self.documents.append(document)

    def add_rule(self, rule: ConfigurationRule) -> None:
        self.rules[rule.key] = rule

    def get_rule(self, key: str, *, verified_only: bool = True) -> ConfigurationRule | None:
        rule = self.rules.get(key)
        if rule is None:
            return None
        if verified_only and rule.status is not VerificationStatus.VERIFIED:
            return None
        return rule

    def require_verified_rule(self, key: str) -> ConfigurationRule:
        rule = self.get_rule(key, verified_only=True)
        if rule is None:
            raise ValueError(f"Verified fabricator rule required: {key}")
        return rule

    def verified_rules(self) -> dict[str, ConfigurationRule]:
        return {
            key: rule
            for key, rule in self.rules.items()
            if rule.status is VerificationStatus.VERIFIED
        }
