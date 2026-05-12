"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.routes import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import engine
from app.middleware.tenant import TenantContextMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Configure process resources for application startup and shutdown."""
    configure_logging()
    logger.info("Starting {app_name} in {environment} mode", app_name=settings.app_name, environment=settings.environment)
    try:
        yield
    finally:
        await engine.dispose()
        logger.success("Shutdown complete for {app_name}", app_name=settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Modular CRM and automation API for MW.AI Data and Systems.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TenantContextMiddleware)

app.include_router(api_router, prefix=settings.api_prefix)

