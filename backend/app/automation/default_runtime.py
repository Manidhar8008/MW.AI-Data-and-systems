from __future__ import annotations

from typing import Any

from .registry import build_default_engine
from .runtime import AutomationRuntime
from .tools import ToolDefinition


def _create_follow_up_task(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_type": "sales_follow_up",
        "customer_name": data["customer_name"],
        "phone": data["phone"],
        "status": "created",
    }


def build_default_runtime() -> AutomationRuntime:
    runtime = AutomationRuntime(engine=build_default_engine())
    runtime.register_tool(
        ToolDefinition(
            id="crm.create_follow_up_task",
            name="Create follow-up task",
            description="Creates a sales follow-up task from a qualified enquiry.",
            handler=_create_follow_up_task,
            allowed_verticals=frozenset({"upvc"}),
        )
    )
    runtime.bind_event("upvc.enquiry.created", "upvc.normalize_enquiry")
    return runtime
