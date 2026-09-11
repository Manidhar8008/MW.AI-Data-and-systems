# MW.AI Master Architecture

## North Star

MW.AI builds AI operating systems for real-world businesses. Each vertical combines a shared operational core with domain-specific AI agents and automations.

## Architecture

```text
MW.AI
├── Core OS
│   ├── Identity & tenancy
│   ├── CRM / customers / companies
│   ├── Tasks & follow-ups
│   ├── Workflow & automation engine
│   ├── Documents & data ingestion
│   ├── Communications / WhatsApp / email
│   ├── Integrations
│   ├── Audit trail & observability
│   └── AI runtime / model adapters
│
└── Vertical OS
    ├── uPVC
    ├── Agriculture
    ├── Construction
    ├── Real Estate
    ├── Manufacturing
    ├── Fabrication
    ├── Solar
    ├── Automotive
    ├── Furniture
    ├── Interiors
    ├── Retail
    ├── Wholesale / Distribution
    ├── Logistics
    ├── Field Service
    ├── Hospitality
    ├── Restaurants
    ├── Clinics
    ├── Education
    ├── Salons
    └── Professional Services
```

## AI Workforce Model

Every vertical models work as agents rather than isolated chatbot features.

```text
Trigger → Intake → Understand → Decide → Execute → Verify → Record → Escalate
```

Each automation must declare:

- trigger
- required inputs
- permissions
- decision policy
- tools/actions
- verification rule
- human approval checkpoint, if required
- failure/escalation path
- audit event
- measurable outcome

## Automation Classification

- **AUTOMATE** — deterministic or bounded work that can execute without human intervention.
- **ASSIST** — AI prepares or recommends work; human approval remains required.
- **HUMAN_REQUIRED** — physical execution, legal accountability, safety-critical judgment, or other work that must remain with a person.

## Vertical Contract

Every vertical should define:

1. customer and lead lifecycle
2. domain entities
3. human roles
4. recurring workflows
5. candidate automations
6. agent definitions
7. integrations
8. domain calculations/rules
9. documents and outputs
10. KPI/ROI measurements

## Product Strategy

Build the shared primitives once. Build vertical depth only where there is a validated workflow and commercial wedge. uPVC is the first deep implementation; other verticals remain registered and can be activated without duplicating the core platform.
