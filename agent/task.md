# PR21: Add focus body camera mode

## Objective

Add a focus-camera mode that follows the currently selected body when the user presses `F`.

## Scope

- add pure focus-camera state with default `none`
- toggle focus using current selection with `F`
- follow focused body by updating camera center each frame
- clear focus when focused body disappears
- clear focus when user drags camera manually
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no new integrator or adaptive timestep changes
- no solar mass multiplier semantic changes
- no absorption model changes
- no source data mutation in `solar_system_data.py`
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/focus_camera.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `tests/test_focus_camera.py`
- `tests/test_overlay_controls.py`
- `README.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/architecture.md`
- `agent/task.md`

## Verification

- run `bash -n scripts/check.sh scripts/test.sh scripts/inspect-diff.sh scripts/rollback.sh`
- run `./scripts/test.sh`
- run `./scripts/check.sh`
- run `./scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- select a body and press `F` to start focus
- press `F` again to clear focus
- verify focused target disappearing clears focus safely
- verify mode/scale/solar-mass/substeps/time/fullscreen controls still work

## Suggested Next PR

`PR22: Add distance scale ruler and preset explanations`
