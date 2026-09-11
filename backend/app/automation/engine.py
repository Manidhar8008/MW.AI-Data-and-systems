from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from .models import AutomationDefinition, AutomationRun, AutomationStatus


class AutomationEngine:
    """Bounded synchronous runtime with tenant context and idempotency hooks."""

    def __init__(self) -> None:
        self._definitions: dict[str, AutomationDefinition] = {}
        self._completed_keys: set[str] = set()

    def register(self, definition: AutomationDefinition) -> None:
        if definition.id in self._definitions:
            raise ValueError(f"Automation already registered: {definition.id}")
        if not definition.vertical:
            raise ValueError("Automation vertical is required")
        if not definition.trigger_event:
            raise ValueError("Automation trigger_event is required")
        self._definitions[definition.id] = definition

    def get(self, automation_id: str) -> AutomationDefinition:
        try:
            return self._definitions[automation_id]
        except KeyError as exc:
            raise KeyError(f"Unknown automation: {automation_id}") from exc

    def list(self, *, vertical: str | None = None) -> list[AutomationDefinition]:
        definitions = self._definitions.values()
        if vertical is not None:
            definitions = (item for item in definitions if item.vertical == vertical)
        return list(definitions)

    def run(
        self,
        automation_id: str,
        input_data: dict[str, Any],
        *,
        tenant_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> AutomationRun:
        definition = self.get(automation_id)
        if idempotency_key and idempotency_key in self._completed_keys:
            return AutomationRun(
                automation_id=automation_id,
                status=AutomationStatus.SUCCEEDED,
                input_data=input_data,
                output_data={"deduplicated": True, "idempotency_key": idempotency_key},
            )

        scoped_input = dict(input_data)
        scoped_input.setdefault("_runtime", {
            "run_id": str(uuid4()),
            "tenant_id": tenant_id,
            "automation_id": automation_id,
        })
        run = AutomationRun(automation_id=automation_id, input_data=scoped_input)
        run.start()
        try:
            output = definition.action(scoped_input)
            run.output_data = output
            if definition.verify is not None and not definition.verify(scoped_input, output):
                run.finish(AutomationStatus.ESCALATED)
                return run
            run.finish(AutomationStatus.SUCCEEDED)
            if idempotency_key:
                self._completed_keys.add(idempotency_key)
            return run
        except Exception as exc:  # runtime must capture action failures
            run.error = str(exc)
            run.finish(AutomationStatus.FAILED)
            return run
