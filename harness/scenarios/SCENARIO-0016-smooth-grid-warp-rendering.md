# SCENARIO-0016: Smooth Field-based Grid Warp

## Goal

Verify PR27 improves warp smoothness while preserving PR25/PR26 behavior boundaries.

## Preconditions

- viewer launches with `python3 -m src.main`
- `W` toggles grid warp
- `G/H/R` control Sun gravity multiplier

## Steps

1. Enter `solar_system` mode and enable warp (`W`).
2. Inspect overview behavior for Sun vs terrestrial planets.
3. Zoom in/out near Earth or Mars slowly.
4. Zoom in near Jupiter and inspect local line continuity.
5. Increase Sun multiplier (`G`) and compare Sun response.

## Expected

- Overview remains Sun-dominant and clean.
- Local warp appears smoothly with zoom fade (no abrupt pop).
- Near-source deformation looks softer, less kinked.
- Multi-source areas remain stable due to influence limiting.
- Sun multiplier strengthens Sun warp only.
