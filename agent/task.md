# PR14: Add fullscreen toggle while preserving resizable window mode

## Objective

Add fullscreen toggle support while preserving existing resizable windowed mode.

## Scope

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- start in windowed resizable mode
- add F11 fullscreen toggle
- add Escape-to-exit-fullscreen behavior
- preserve camera/overlay/trails/labels/selection/inspector/time-control compatibility
- keep display mode changes separate from simulation state
- add non-window tests for display mode state logic

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no save/load display settings
- no complex display manager
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
- keep display mode logic pure and testable
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/display_modes.py`
- `src/universe/rendering.py` only if status/surface compatibility needs it
- `src/universe/overlay_controls.py` only if layout needs it
- `tests/test_render_scale.py`
- `tests/test_selection.py`
- `tests/test_inspector.py`
- `tests/test_time_controls.py`
- `tests/test_trails.py`
- `tests/test_overlay_controls.py`
- `tests/test_display_modes.py`
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
- optionally verify F11 fullscreen toggle and windowed restore behavior

## Suggested Next PR

`PR15: Convert overlay toggles into checkbox-style controls`
