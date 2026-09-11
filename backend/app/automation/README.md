# Automation Engine v0

The first implementation provides a deliberately small execution kernel:

- register automation definitions
- filter definitions by vertical
- execute a bounded action
- verify output
- capture success/failure/escalation state
- retain input/output and timestamps for later persistence

## First vertical action

`upvc.normalize_enquiry` accepts a uPVC enquiry, validates required fields and dimensions, normalizes the payload, and marks it qualified. Its declared next stage is the engineering validation workflow.

## Production evolution

This kernel will later connect to:

- PostgreSQL persistence
- event bus / durable queue
- tenant authorization
- tool registry
- AI model adapter
- workflow scheduling
- idempotency keys
- retry policy
- audit/event store
- human approval tasks

Do not put provider-specific AI calls directly into domain actions. Keep model providers behind the AI runtime/tool interfaces.
