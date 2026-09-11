from __future__ import annotations

from typing import Any

from .models import AutomationDefinition, AutomationRun, AutomationStatus


class AutomationEngine:
    """Small synchronous runtime for bounded business automations.

    The engine deliberately keeps orchestration separate from domain actions.
    Domain-specific agents/tools are injected through AutomationDefinition.
    """

    def __init__(self) -> None:
        self._definitions: dict[str, AutomationDefinition] = {}

    def register(self, definition: AutomationDefinition) -> None:
        if definition.id in self._definitions:
            raise ValueError(f"Automation already registered: {definition.id}")
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

    def run(self, automation_id: str, input_data: dict[str, Any]) -> AutomationRun:
        definition = self.get(automation_id)
        run = AutomationRun(automation_id=automation_id, input_data=input_data)
        run.start()

        try:
            output = definition.action(input_data)
            run.output_data = output

            if definition.verify is not None and not definition.verify(input_data, output):
                run.finish(AutomationStatus.ESCALATED)
                return run

            run.finish(AutomationStatus.SUCCEEDED)
            return run
        except Exception as exc:  # noqa: BLE001 - runtime must capture action failures
            run.error = str(exc)
            run.finish(AutomationStatus.FAILED)
            return run
