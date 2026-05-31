# PR12: Extend inspector for real solar-system body fields

## Objective

Extend the read-only selected-body inspector with real solar-system fields and source transparency.

## Scope

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- extend inspector output for selected bodies
- include mode, source, and local-dataset-backed solar-system fields where available
- preserve selection/overlay/time-control compatibility
- keep inspector read-only
- add non-window tests for inspector behavior

## Non-Goals

- no Newtonian equation changes
- no new integrator
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
- keep inspector logic pure and testable
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/rendering.py`
- `src/universe/selection.py`
- `src/universe/inspector.py`
- `src/universe/body.py` only if inspector metadata exposure is needed
- `src/universe/demo_simulation.py`
- `src/universe/solar_system_simulation.py`
- `src/universe/solar_system_data.py` only if metadata access cleanup is needed
- `tests/test_inspector.py`
- `tests/test_solar_system_simulation.py`
- `tests/test_solar_system_data.py`
- `tests/test_render_scale.py`
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
- optionally verify controlled_demo and solar_system inspector field display

## Suggested Next PR

`PR13: Improve trails with dashed body-colored paths`
