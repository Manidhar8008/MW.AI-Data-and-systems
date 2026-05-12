"""Tenant isolation middleware."""

from collections.abc import Awaitable, Callable

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Require a tenant header for tenant-owned API routes."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """Attach tenant context to the request state when required."""
        if self._requires_tenant(request.url.path):
            tenant_id = request.headers.get("X-Tenant-ID", "").strip()
            if not tenant_id:
                logger.warning("Rejected tenant-scoped request without X-Tenant-ID: {path}", path=request.url.path)
                return JSONResponse(
                    status_code=400,
                    content={"detail": "X-Tenant-ID header is required for tenant-scoped API routes."},
                )
            request.state.tenant_id = tenant_id
        else:
            request.state.tenant_id = None

        try:
            return await call_next(request)
        except Exception as exc:
            logger.error("Unhandled request failure on {path}: {error}", path=request.url.path, error=str(exc))
            raise

    @staticmethod
    def _requires_tenant(path: str) -> bool:
        """Return whether a request path must include tenant context."""
        public_paths = (
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/health",
        )
        return path.startswith("/api/") and not any(path.startswith(public_path) for public_path in public_paths)

