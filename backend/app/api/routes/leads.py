"""Lead management routes."""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.lead import LeadCreate, LeadRead
from app.services.lead_service import LeadService
from app.utils.tenant import get_tenant_id

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=list[LeadRead])
async def list_leads(
    request: Request,
    db_session: AsyncSession = Depends(get_db_session),
) -> list[LeadRead]:
    """List leads scoped to the active tenant."""
    tenant_id = get_tenant_id(request)
    service = LeadService(db_session)
    leads = await service.list_leads(tenant_id=tenant_id)
    return [LeadRead.model_validate(lead) for lead in leads]


@router.post("", response_model=LeadRead, status_code=status.HTTP_201_CREATED)
async def create_lead(
    payload: LeadCreate,
    request: Request,
    db_session: AsyncSession = Depends(get_db_session),
) -> LeadRead:
    """Create a lead scoped to the active tenant."""
    tenant_id = get_tenant_id(request)
    service = LeadService(db_session)
    lead = await service.create_lead(tenant_id=tenant_id, payload=payload)
    return LeadRead.model_validate(lead)

