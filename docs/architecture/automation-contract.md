# MW.AI Automation Contract

Every executable automation in MW.AI must be representable by this contract.

```yaml
id: unique-automation-id
vertical: vertical-id
name: Human-readable name
classification: AUTOMATE | ASSIST | HUMAN_REQUIRED
trigger:
  event: domain.event
  conditions: []
inputs: []
permissions: []
decision_policy:
  rules: []
actions: []
verification:
  checks: []
escalation:
  conditions: []
  destination: human-role-or-agent
audit:
  events: []
outcomes:
  metrics: []
```

## Runtime lifecycle

1. Receive a trusted trigger.
2. Resolve tenant and authorization context.
3. Load required domain state and memory.
4. Apply deterministic rules before model reasoning where possible.
5. Ask an AI agent for bounded reasoning when required.
6. Execute only authorized tools/actions.
7. Verify the resulting state.
8. Record the action and outcome in the audit trail.
9. Escalate when verification fails, confidence/policy thresholds are not met, or human approval is required.

## Design rule

An AI agent is not considered an automation merely because it generates text. An automation must produce a controlled, observable business action or a clearly reviewable decision artifact.
