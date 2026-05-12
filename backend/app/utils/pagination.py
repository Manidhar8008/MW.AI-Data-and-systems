"""Pagination helpers for list endpoints."""

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Validated pagination parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=25, ge=1, le=100)

    @property
    def offset(self) -> int:
        """Return SQL offset for the current page."""
        return (self.page - 1) * self.page_size

