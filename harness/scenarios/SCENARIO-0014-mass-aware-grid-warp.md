# SCENARIO-0014: Mass-aware Grid Warp Hierarchy

## Goal

Verify PR25 suppresses misleading low-mass overview warp while preserving Sun-dominant visual response.

## Preconditions

- viewer launches with `python3 -m src.main`
- grid warp can be toggled with `W`

## Steps

1. Switch to `solar_system` mode (`M`) and enable warp (`W`).
2. Move to an overview-style camera view (`B` if needed).
3. Observe relative warp prominence across Sun/Jupiter/terrestrial planets.
4. Increase Sun gravity multiplier (`G`) and compare Sun warp change.

## Expected

- Sun warp is dominant in overview.
- Jupiter/Saturn are weaker than Sun.
- Earth/Mars/Venus/Mercury are suppressed or barely visible in overview.
- Raising Sun multiplier strengthens Sun warp only.
- No traceback occurs and controls remain compatible.
