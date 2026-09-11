from __future__ import annotations

from typing import Any

from .engine import AutomationEngine
from .events import Event, EventBus
from .models import AutomationRun
from .tools import ToolDefinition, ToolRegistry


class AutomationRuntime:
    """Composition root connecting event triggers, automations and tools."""

    def __init__(self, engine: AutomationEngine | None = None) -> None:
        self.events = EventBus()
        self.engine = engine or AutomationEngine()
        self.tools = ToolRegistry()

    def bind_event(self, event_name: str, automation_id: str) -> None:
        def handler(event: Event) -> None:
            self.engine.run(automation_id, event.payload)

        self.events.subscribe(event_name, handler)

    def register_tool(self, tool: ToolDefinition) -> None:
        self.tools.register(tool)

    def emit(self, name: str, payload: dict[str, Any], tenant_id: str | None = None) -> Event:
        event = Event(name=name, payload=payload, tenant_id=tenant_id)
        self.events.publish(event)
        return event

    def run_tool(
        self,
        tool_id: str,
        payload: dict[str, Any],
        *,
        vertical: str,
        human_approved: bool = False,
    ) -> dict[str, Any]:
        return self.tools.execute(
            tool_id,
            payload,
            vertical=vertical,
            human_approved=human_approved,
        )
