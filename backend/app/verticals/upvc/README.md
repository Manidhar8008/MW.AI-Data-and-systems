# MW.AI uPVC Fabrication Brain

The uPVC vertical exposes a deterministic production pipeline:

```text
Configuration
  -> Engineering
  -> Commercial BOM
  -> Profile decomposition
  -> Glass dimensions
  -> Reinforcement schedule
  -> Hardware schedule
  -> Cut lists
  -> 1D stock optimization
  -> Production Order
```

## Fabrication rules

`FabricationRules` and `ProfileRule` contain configurable system parameters:

- profile codes and stock lengths
- frame/sash allowances
- glazing clearance
- reinforcement threshold and stock length
- hardware quantities
- saw kerf

The defaults are intentionally generic. A production tenant must load approved profile-system and hardware rules before the resulting cut plan is treated as manufacturing authority.

## Traceability

Every cut piece retains a source such as `outer_frame_width` or `sash_1_height`. The production order contains the configuration id plus engineering, glass, reinforcement, hardware and optimized cut plans.

## Optimization

The current optimizer is deterministic first-fit-decreasing and accounts for saw kerf. It reports stock consumed, usable piece length, kerf, waste and utilization.

This is a baseline optimizer, not CNC/saw-machine-specific nesting. Future machine adapters can consume the same `ProductionOrder` contract.
