# SCENARIO-0008: Camera View Presets

## Goal

Verify runtime camera view preset controls for PR19 without changing simulation physics.

## Preconditions

- Launch with `python3 -m src.main`
- Overlay is visible

## Steps

1. Confirm overlay shows `View: normal` at startup.
2. Press `B` once; confirm overlay changes to `View: overview`.
3. Press `B` again; confirm overlay changes to `View: close`.
4. Press `B` again; confirm overlay cycles back to `View: normal`.
5. Pan/zoom camera away from default, then press `0`; confirm camera resets to the current preset baseline.
6. Press `M`, `V`, `G`, `H`, `R`, `Space`, and `F11` once each; confirm no traceback and controls remain responsive.

## Expected Result

- Preset cycle is deterministic: `normal -> overview -> close -> normal`
- `0` resets camera view only (simulation mode, solar mass experiment state, and selection state are preserved)
- No physics-logic regression is implied by camera preset interaction
