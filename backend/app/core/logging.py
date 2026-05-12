"""Loguru logging configuration."""

import sys

from loguru import logger

from app.core.config import settings


def configure_logging() -> None:
    """Configure structured terminal logging for local development."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.log_level,
        backtrace=False,
        diagnose=settings.environment == "local",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> | {message}",
    )

