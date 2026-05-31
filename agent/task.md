# PR8: Add basic body selection inspector without changing physics simulation

## Objective

Add a simple read-only inspector for selected controlled-demo bodies without changing physics correctness.

## Scope

- add runtime selection state (`selected_body_name`)
- add render-space body hit testing
- support click-to-select behavior for demo bodies
- add read-only inspector lines for selected body (name, mass, position, velocity)
- add visual selection indicator around selected body
- preserve input priority: overlay controls > body selection > camera drag
- add non-window tests for selection and inspector formatting logic

## Non-Goals

- no Newtonian equation changes
- no body dragging
- no body editing
- no stable real solar-system tuning claims
- no real ephemeris or JPL Horizons runtime integration
- no hardcoded circular orbit animation
- no Lorentz factor
- no grid distortion
- no fullscreen mode
- no UI framework

## Required Design

- launch with `python3 -m src.main`
- preserve camera drag, zoom, and dynamic grid behavior
- keep selection/inspector state in runtime/rendering control paths only
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/rendering.py`
- `src/universe/selection.py`
- `src/universe/overlay_controls.py` only if needed for input-priority integration
- `src/universe/demo_simulation.py` only if needed for data handoff
- `tests/test_selection.py`
- `tests/test_overlay_controls.py`
- `tests/test_demo_simulation.py`
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
- verify viewer launches
- verify overlay toggles remain visible and clickable
- verify clicking demo bodies selects and highlights them
- verify inspector panel updates with selected body data
- verify clicking background clears selection
- verify background drag still works
- verify mouse-wheel zoom still works

## Suggested Next Work

Demand-driven optimization or bugfix PRs defined by the human.
