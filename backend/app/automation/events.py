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
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


EventHandler = Callable[[Event], None]


class EventBus:
    """Minimal synchronous event bus for the first runtime slice.

    The interface is intentionally small so it can later be backed by a durable
    queue without changing domain publishers or subscribers.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_name, []).append(handler)

    def publish(self, event: Event) -> None:
        for handler in tuple(self._handlers.get(event.name, ())):
            handler(event)

    def handler_count(self, event_name: str) -> int:
        return len(self._handlers.get(event_name, ()))
