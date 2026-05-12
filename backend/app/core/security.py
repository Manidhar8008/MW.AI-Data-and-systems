"""Password hashing and JWT helper functions."""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a stored password hash."""
    return bool(password_context.verify(plain_password, hashed_password))


def hash_password(password: str) -> str:
    """Hash a password for durable storage."""
    return str(password_context.hash(password))


def create_access_token(subject: str, tenant_id: str, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token."""
    expiry = datetime.now(tz=UTC) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    payload: dict[str, Any] = {
        "sub": subject,
        "tenant_id": tenant_id,
        "exp": expiry,
    }
    return str(jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm))

