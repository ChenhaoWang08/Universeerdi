# PR19: Add camera zoom range controls and view presets

## Objective

Add runtime camera view controls so users can switch between useful zoom/view presets without editing source code.

## Scope

- add pure camera view preset state for `normal`, `overview`, and `close`
- support deterministic preset cycling
- support reset to current preset defaults
- make camera zoom step configurable per camera state
- expose camera view status in the overlay
- keep behavior deterministic and testable without opening a window
- preserve compatibility with mode/scale/time/fullscreen/selection/solar-mass controls

## Non-Goals

- no Newtonian equation changes
- no new physics integrator or substep logic
- no changes to `solar_system_data.py`
- no solar mass multiplier behavior changes
- no absorption behavior changes
- no focus-body camera follow
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/camera_views.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `tests/test_camera_views.py`
- `tests/test_camera.py`
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
- verify viewer launches
- verify `B` cycles view preset status in overlay
- verify `0` resets camera to current preset
- verify camera drag and wheel zoom still work
- verify mode/scale/solar-mass/time/fullscreen controls still work

## Suggested Next PR

`PR20: Add physics substeps for high-gravity stability`
