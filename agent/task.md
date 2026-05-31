# PR10: Add pause, resume, and time scale controls

## Objective

Add runtime pause/resume, bounded time scale, and dt clamp controls without changing Newtonian equations.

## Scope

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- add pause/resume state
- add bounded time scale controls
- clamp frame dt before scaling
- display running/paused plus scale in overlay
- add non-window tests for time controls

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no long-term stability guarantee claims
- no Lorentz factor
- no grid distortion
- no fullscreen mode
- no high-precision ephemeris/JPL integration

## Required Design

- launch with `python3 -m src.main`
- preserve existing overlay/selection/camera behavior
- keep physics stepping via existing simulation/physics path
- keep time-control logic pure and testable
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/time_controls.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py` only if overlay layout needs adjustment
- `src/universe/demo_simulation.py` only if dt handoff compatibility needs it
- `src/universe/solar_system_simulation.py` only if dt handoff compatibility needs it
- `tests/test_time_controls.py`
- `tests/test_demo_simulation.py`
- `tests/test_solar_system_simulation.py`
- `tests/test_overlay_controls.py`
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
- optionally verify pause/resume and time-scale keys in runtime

## Suggested Next PR

`PR11: Add physical-to-render scale policy and minimum visible radius`
