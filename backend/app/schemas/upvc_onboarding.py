from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.verticals.upvc.onboarding import VerificationStatus, RuleSource


class OnboardingInitialize(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)


class RuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: Any
    source: RuleSource
    confidence: float
    status: VerificationStatus
    source_document_id: str | None = None


class DocumentRead(BaseModel):
    id: str
    name: str
    document_type: str
    source_uri: str | None = None


class OnboardingRead(BaseModel):
    tenant_id: str
    company_name: str
    documents: list[DocumentRead]
    rules: list[RuleRead]
    readiness: dict[str, Any]


class RuleAction(BaseModel):
    """Explicit owner review action for a candidate rule."""

    action: str = Field(pattern="^(verify|reject)$")
