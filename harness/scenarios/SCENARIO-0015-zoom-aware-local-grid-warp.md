# SCENARIO-0015: Zoom-aware Local Grid Warp

## Goal

Verify PR26 keeps overview suppression while enabling local small-body warp visibility at close zoom.

## Preconditions

- viewer launches with `python3 -m src.main`
- `W` toggles grid warp
- `G/H/R` still control Sun gravity multiplier

## Steps

1. Enter `solar_system` mode and enable warp (`W`).
2. Stay zoomed out (overview) and inspect Earth/Mars/Venus/Mercury warp visibility.
3. Zoom in close to Mars or Earth.
4. Compare local grid behavior around that body.
5. Increase Sun multiplier (`G`) and confirm Sun response.

## Expected

- Overview remains Sun-dominant; small planets are suppressed.
- Close zoom can show small local warp around low-mass planets.
- Local warp stays visually local and bounded.
- Sun multiplier strengthens Sun warp only.
- No traceback and controls remain compatible.
