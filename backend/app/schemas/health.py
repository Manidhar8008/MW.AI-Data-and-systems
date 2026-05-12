"""Health response schemas."""

from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """API health response."""

    status: str
    app_name: str
    environment: str
    checked_at: datetime

