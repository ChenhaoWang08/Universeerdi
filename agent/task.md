# PR6: Add visual trails and labels behind feature flags

## Objective

Add optional visual trails and body labels to the controlled demo simulation without changing physics correctness.

## Scope

- add optional trail rendering for controlled demo bodies
- add optional body label rendering for controlled demo bodies
- keep both overlays behind simple feature flags in runtime configuration
- keep feature work in rendering/runtime layers only
- preserve PR5 controlled demo stepping behavior
- add non-window tests for trail/label helper logic

## Non-Goals

- no changes to Newtonian equations
- no stable real solar-system tuning claims
- no real ephemeris or JPL Horizons runtime integration
- no hardcoded circular orbit animation
- no Lorentz factor
- no grid distortion
- no fullscreen mode
- no complex UI framework

## Required Design

- launch with `python3 -m src.main`
- preserve camera drag, zoom, and grid behavior
- keep trails bounded with a fixed history length
- keep labels and trails optional via feature flags
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/rendering.py`
- `src/universe/demo_simulation.py` (only if integration requires minor changes)
- `tests/test_grid.py`
- `tests/test_demo_simulation.py` (only if integration requires minor checks)
- `README.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/architecture.md`
- `agent/task.md`
- `harness/scenarios/`
- `harness/judges/`

## Forbidden Files

- `.env`
- `.env.*`
- `secrets/`
- deployment files
- `.github/workflows/`
- external API configuration
- binary assets
- credentials
- tokens

## Verification

- run `bash -n scripts/check.sh scripts/test.sh scripts/inspect-diff.sh scripts/rollback.sh`
- run `scripts/check.sh`
- run `scripts/test.sh`
- run `scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- verify window opens and closes cleanly
- verify grid remains visible
- verify camera drag and zoom remain available
- verify trails and labels appear when flags are enabled

## Suggested Next PR

`PR7: Add configurable overlay styling controls without changing simulation correctness`
