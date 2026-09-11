# Event + Tool Layer

The automation runtime now has three explicit primitives:

```text
EventBus → AutomationEngine → ToolRegistry
   │              │                │
 trigger       workflow          bounded action
```

## Events

`Event` carries a unique event id, event name, tenant id, payload, and UTC occurrence timestamp.

`EventBus` provides subscription and publication. This first version is in-process and synchronous by design; the interface can later be backed by a durable queue.

## Tools

`ToolRegistry` exposes bounded business actions. Every tool declares a stable id, description, handler, allowed verticals, and optional human approval requirement.

The registry rejects calls from unauthorized verticals and blocks approval-gated actions until explicitly approved.

## Runtime composition

`AutomationRuntime` wires event triggers to automation definitions and exposes controlled tool execution. Domain code should publish business events and invoke registered tools rather than coupling itself to infrastructure providers.

## Current uPVC slice

```text
upvc.enquiry.created
        ↓
upvc.normalize_enquiry
        ↓
qualified enquiry
        ↓
(next: engineering validation)
```

Available tool: `crm.create_follow_up_task`.

This is intentionally a thin vertical-specific tool. CRM persistence, durable queues, idempotency, audit persistence and external integrations are subsequent layers.
