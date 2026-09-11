# MW.AI uPVC Fabrication Pipeline

```text
Configuration
  ↓
Engineering validation
  ↓
BOM
  ↓
Profile decomposition
  ├── frame members
  └── sash members
  ↓
Glass dimensions
  ↓
Reinforcement schedule
  ↓
Hardware schedule
  ↓
Cut lists
  ↓
1D stock cutting optimizer
  ↓
Production order
```

## Deterministic rules

The planner uses explicit `FabricationRules` and `PriceBook` inputs. It does not infer manufacturer-specific fabrication dimensions. Generic offsets, stock lengths and reinforcement thresholds are configuration defaults and must be replaced by approved system rules for live production.

## Cutting optimization

The first optimizer uses a deterministic first-fit-decreasing packing strategy. Every required cut is sorted from longest to shortest and placed into the first stock bar with enough remaining length. The resulting `CutPlan` records stock bars, cuts, offcuts, total piece length and utilization.

This is a baseline optimization layer. A later optimizer can add kerf, end trimming, saw constraints, profile-specific nesting, remnant inventory and multi-order batch optimization.

## Production order

`ProductionOrder` preserves:

- configuration id
- engineering validity
- fabrication line items
- glass pieces and dimensions
- reinforcement pieces
- hardware schedule
- profile cut plan
- reinforcement cut plan
- engineering warnings

The order is marked `ready_for_production` only after engineering validation succeeds.
