"""Lead request and response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LeadBase(BaseModel):
    """Common lead fields."""

    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=6, max_length=32)
    source: str = Field(default="manual", min_length=2, max_length=64)
    status: str = Field(default="new", min_length=2, max_length=32)
    notes: str | None = Field(default=None, max_length=4000)


class LeadCreate(LeadBase):
    """Payload for creating a lead."""


class LeadRead(LeadBase):
    """Lead response returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: datetime

