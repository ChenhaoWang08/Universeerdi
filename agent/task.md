# PR23: Add trail reset and trail length controls

## Objective

Add runtime controls to clear trail history and adjust trail history length safely.

## Scope

- add pure trail-control state with fixed length values
- add runtime controls:
  - `C` clear trail history
  - `,` decrease trail length
  - `.` increase trail length
- trim existing history immediately when reducing length
- keep rendering style unchanged (dashed + body-colored)
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no solar mass / absorption / substep behavior changes
- no focus camera / camera preset / render-scale behavior changes
- no source data mutation in `solar_system_data.py`
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/trail_controls.py`
- `src/universe/trails.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `tests/test_trail_controls.py`
- `tests/test_trails.py`
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
- verify `C` clears trails
- verify `,` and `.` adjust trail history length
- verify existing controls remain compatible

## Suggested Next PR

`PR24: Add help overlay for controls`
