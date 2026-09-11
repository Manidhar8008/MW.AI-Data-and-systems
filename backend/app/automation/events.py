from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4


@dataclass(frozen=True)
class Event:
    name: str
    payload: dict[str, Any]
    tenant_id: str | None = None
    correlation_id: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class EventDispatchFailure:
    event_id: str
    event_name: str
    error: str


EventHandler = Callable[[Event], None]


class EventBus:
    """Synchronous bus with deterministic ordering and failure isolation."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}
        self._failures: list[EventDispatchFailure] = []

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        if not event_name:
            raise ValueError("event_name is required")
        self._handlers.setdefault(event_name, []).append(handler)

    def publish(self, event: Event) -> tuple[EventDispatchFailure, ...]:
        failures: list[EventDispatchFailure] = []
        for handler in tuple(self._handlers.get(event.name, ())):
            try:
                handler(event)
            except Exception as exc:  # noqa: BLE001 - one subscriber must not stop others
                failure = EventDispatchFailure(event.id, event.name, str(exc))
                failures.append(failure)
                self._failures.append(failure)
        return tuple(failures)

    def handler_count(self, event_name: str) -> int:
        return len(self._handlers.get(event_name, ()))

    def failures(self) -> tuple[EventDispatchFailure, ...]:
        return tuple(self._failures)
