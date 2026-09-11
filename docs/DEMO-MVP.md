# MW.AI × uPVC — Demo MVP

## Purpose

The demo proves one complete fabricator workflow:

```text
Customer enquiry
→ Project
→ Configuration
→ Engineering
→ Quote
→ Approval
→ Production Order
→ Workshop state
→ Exception
→ Installation
→ Completed
```

The demo is intentionally narrower than the full uPVC operating system. Real integrations such as telephony, WhatsApp, machine telemetry, and computer vision can be represented by deterministic demo events until those integrations are implemented.

## Demo tenant

The demo uses one tenant configuration and one order. All tenant-specific commercial and production rules must come from verified configuration; no manufacturer pricing or fabrication rule should be invented in the UI.

## Five-screen demo

1. **AI Operations Dashboard** — active projects, quotes awaiting approval, production jobs, installations, exceptions, and the AI employee activity feed.
2. **Customer / Project** — customer details, site, reference photo, opening list, and measurements.
3. **Engineering / Quote** — configuration, profile system, glass, SFT area, BOM summary, quote total, and customer approval action.
4. **Production** — stage timeline, expected vs observed production, material consumption, waste, and exceptions.
5. **Fabricator Configuration** — verified profile systems, pricing rules, documents, and readiness status.

## Golden-path order

Use `MW-ORD-0001` as the canonical demonstration order. Its values should be seeded only from explicitly supplied demo facts or verified onboarding data.

## Demo extraction track

During implementation, extract only facts needed to make the golden path credible:

- company identity
- supported product types
- profile systems
- SFT pricing
- glass pricing
- hardware pricing
- installation / transport / tax rules
- required engineering constraints
- stock lengths
- QC checklist
- communication channels

Every extracted fact is either:

```text
PENDING → VERIFIED → ACTIVE
```

or remains unavailable to money/production logic.

## Safety boundary

Verified measurements must never directly create cutting instructions. The production chain is:

```text
Measurement
→ Configuration
→ Engineering validation
→ BOM
→ Quote / approval
→ Production Order
→ Cut List
→ Cutting
```

## Camera simulation

The demo may emit synthetic production observations such as:

```text
Expected profile pieces: 24
Observed: 18
Unobserved: 6
Estimated waste: 2.4 m
Estimated waste value: ₹576
```

These are demo events only until camera intelligence is implemented.

## Definition of done

A demo is ready when one can start at a customer enquiry and finish at completed installation while the UI visibly demonstrates:

- tenant-specific configuration
- deterministic engineering/BOM/quote calculations
- customer approval
- production state transitions
- expected-vs-observed reconciliation
- an actionable exception
- an AI employee activity stream
