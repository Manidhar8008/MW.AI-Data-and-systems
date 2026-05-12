"""Lead business logic."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app.schemas.lead import LeadCreate


class LeadService:
    """Coordinate tenant-scoped lead persistence."""

    def __init__(self, db_session: AsyncSession) -> None:
        """Initialize the service with an async database session."""
        self.db_session = db_session

    async def list_leads(self, tenant_id: str) -> Sequence[Lead]:
        """Return leads for a single tenant only."""
        statement = select(Lead).where(Lead.tenant_id == tenant_id).order_by(Lead.created_at.desc())
        result = await self.db_session.execute(statement)
        return result.scalars().all()

    async def create_lead(self, tenant_id: str, payload: LeadCreate) -> Lead:
        """Create and persist a lead for a single tenant."""
        lead = Lead(
            tenant_id=tenant_id,
            name=payload.name,
            phone=payload.phone,
            source=payload.source,
            status=payload.status,
            notes=payload.notes,
        )
        self.db_session.add(lead)
        await self.db_session.commit()
        await self.db_session.refresh(lead)
        return lead

