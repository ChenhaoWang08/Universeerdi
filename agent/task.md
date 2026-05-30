# PR7: Add simple in-window toggle controls for labels and trails

## Objective

Add simple clickable in-window controls for toggling labels and trails in controlled demo mode, while keeping physics correctness unchanged.

## Scope

- add runtime overlay control state for `show_labels` and `show_trails`
- render simple top-left controls for Labels and Trails ON/OFF
- handle click interactions for toggle controls
- ensure control clicks are consumed before camera drag logic
- keep overlay toggles rendering-only and separate from physics state
- add non-window tests for overlay control hitboxes and click behavior

## Non-Goals

- no changes to Newtonian equations
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
- maintain bounded trail history
- keep toggle state local to runtime/rendering control paths
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `src/universe/demo_simulation.py` only if needed for small handoff changes
- `tests/test_grid.py`
- `tests/test_overlay_controls.py`
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
- verify Labels and Trails toggles are visible
- verify clicking toggles changes overlay visibility
- verify clicking controls does not pan the camera
- verify dragging background still pans camera
- verify scroll wheel zoom still works

## Suggested Next PR

`PR8: Add a basic body selection inspector without changing physics simulation correctness`
