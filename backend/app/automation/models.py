from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable


class AutomationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ESCALATED = "escalated"


@dataclass(frozen=True)
class AutomationDefinition:
    id: str
    vertical: str
    name: str
    classification: str
    trigger_event: str
    action: Callable[[dict[str, Any]], dict[str, Any]]
    verify: Callable[[dict[str, Any], dict[str, Any]], bool] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AutomationRun:
    automation_id: str
    status: AutomationStatus = AutomationStatus.PENDING
    input_data: dict[str, Any] = field(default_factory=dict)
    output_data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None

    def start(self) -> None:
        self.status = AutomationStatus.RUNNING
        self.started_at = datetime.now(timezone.utc)

    def finish(self, status: AutomationStatus) -> None:
        self.status = status
        self.finished_at = datetime.now(timezone.utc)
