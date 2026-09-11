"""Versioned API route composition."""

from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.leads import router as leads_router
from app.api.routes.upvc_onboarding import router as upvc_onboarding_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(leads_router)
api_router.include_router(upvc_onboarding_router)

