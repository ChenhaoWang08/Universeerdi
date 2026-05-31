# PR13: Improve trails with dashed body-colored paths

## Objective

Improve trail readability with dashed body-colored paths while keeping trails rendering-only.

## Scope

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- render trails using body color or safe fallback
- support dashed trail rendering
- keep trail history bounded
- preserve labels/selection/inspector/time-control compatibility
- keep trails rendering-only
- add non-window tests for trail helpers

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no orbit prediction or hardcoded circular animation
- no physical mass/position/velocity/radius mutation
- no body editing or dragging
- no long-term stability guarantee claims
- no Lorentz factor
- no grid distortion
- no fullscreen mode
- no high-precision ephemeris/JPL integration

## Required Design

- launch with `python3 -m src.main`
- preserve existing overlay/selection/time-control/camera behavior
- keep physics stepping unchanged through existing simulation/physics path
- keep trail geometry/history logic pure and testable
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/rendering.py`
- `src/universe/trails.py`
- `src/universe/body.py` only if color access compatibility is needed
- `tests/test_render_scale.py`
- `tests/test_selection.py`
- `tests/test_inspector.py`
- `tests/test_time_controls.py`
- `tests/test_trails.py`
- `README.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/architecture.md`
- `agent/task.md`

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
- verify viewer launches
- verify no immediate traceback
- optionally verify dashed trails, body-color trails, and show_trails toggle behavior

## Suggested Next PR

`PR14: Add fullscreen toggle while preserving resizable window mode`
