# SCENARIO-0011: Distance Scale Ruler

## Goal

Verify PR22 informational ruler and preset explanation behavior.

## Preconditions

- Launch with `python3 -m src.main`

## Steps

1. Switch to `solar_system` mode with `M`.
2. Confirm bottom-left distance ruler appears with a distance label.
3. Press `V` to cycle render-scale presets and confirm scale-note text changes.
4. Scroll zoom and confirm ruler label updates with zoom level.
5. Switch back to `controlled_demo` and confirm solar-system ruler is hidden.

## Expected Result

- Ruler and scale-note are visible in `solar_system` mode.
- Ruler text is understandable (m/km/AU) and deterministic.
- Ruler is informational only and does not alter controls or simulation behavior.
