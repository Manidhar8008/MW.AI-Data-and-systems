"""Tenant context helpers."""

from fastapi import HTTPException, Request, status


def get_tenant_id(request: Request) -> str:
    """Return the tenant identifier attached by middleware."""
    tenant_id = getattr(request.state, "tenant_id", None)
    if not isinstance(tenant_id, str) or not tenant_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context is missing.",
        )
    return tenant_id.strip()

