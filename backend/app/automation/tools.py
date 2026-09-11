from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class ToolDefinition:
    id: str
    name: str
    description: str
    handler: ToolHandler
    allowed_verticals: frozenset[str] = frozenset()
    requires_human_approval: bool = False


class ToolRegistry:
    """Registry for bounded actions available to automations and agents."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.id in self._tools:
            raise ValueError(f"Tool already registered: {tool.id}")
        self._tools[tool.id] = tool

    def get(self, tool_id: str) -> ToolDefinition:
        try:
            return self._tools[tool_id]
        except KeyError as exc:
            raise KeyError(f"Unknown tool: {tool_id}") from exc

    def list(self, *, vertical: str | None = None) -> list[ToolDefinition]:
        tools = self._tools.values()
        if vertical is not None:
            tools = (
                tool for tool in tools
                if not tool.allowed_verticals or vertical in tool.allowed_verticals
            )
        return list(tools)

    def execute(
        self,
        tool_id: str,
        input_data: dict[str, Any],
        *,
        vertical: str,
        human_approved: bool = False,
    ) -> dict[str, Any]:
        tool = self.get(tool_id)
        if tool.allowed_verticals and vertical not in tool.allowed_verticals:
            raise PermissionError(f"Tool {tool_id} is not enabled for vertical {vertical}")
        if tool.requires_human_approval and not human_approved:
            raise PermissionError(f"Tool {tool_id} requires human approval")
        return tool.handler(input_data)
