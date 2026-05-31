# PR11: Add physical-to-render scale policy and minimum visible radius

## Objective

Add explicit display-only render scaling for physical position/radius mapping without changing Newtonian equations.

## Scope

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- add render-scale policy model
- map physical position to render/world coordinates
- map physical radius to visible radius with min/max clamps
- keep selection compatibility with rendered radius
- add non-window tests for render-scale behavior

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no physical mass/position/velocity/radius mutation for visual tuning
- no long-term stability guarantee claims
- no Lorentz factor
- no grid distortion
- no fullscreen mode
- no high-precision ephemeris/JPL integration

## Required Design

- launch with `python3 -m src.main`
- preserve existing overlay/selection/time-control/camera behavior
- keep physics stepping unchanged through existing simulation/physics path
- keep render-scale logic pure and testable
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/rendering.py`
- `src/universe/selection.py`
- `src/universe/render_scale.py`
- `src/universe/body.py` only if render-radius metadata exposure is needed
- `src/universe/demo_simulation.py`
- `src/universe/solar_system_simulation.py`
- `tests/test_render_scale.py`
- `tests/test_demo_simulation.py`
- `tests/test_solar_system_simulation.py`
- `tests/test_selection.py`
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
- optionally verify readable solar-system rendering and selection compatibility

## Suggested Next PR

`PR12: Extend inspector for real solar-system body fields`
