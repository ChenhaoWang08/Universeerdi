# SCENARIO-0009: Physics Substeps

## Goal

Verify PR20 fixed physics substeps behavior in `solar_system` mode.

## Preconditions

- Launch with `python3 -m src.main`
- Switch to `solar_system` mode with `M`

## Steps

1. Confirm overlay shows `Substeps: 1` initially.
2. Press `=` repeatedly and confirm `Substeps` increases up to max.
3. Press `-` repeatedly and confirm `Substeps` decreases down to min.
4. Increase Sun gravity (`G`) and compare behavior at `Substeps: 1` vs higher substeps.
5. Confirm no traceback while using `B`, `0`, `V`, `Space`, `F11`.

## Expected Result

- Substep status is deterministic and bounded.
- Solar-system stepping remains responsive.
- Absorption under high gravity appears less jumpy with larger substeps.
- No physics-equation or source-data mutation is implied by control changes.
