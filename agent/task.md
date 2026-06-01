# PR28: Add right-click spawn menu and settings panel shell

## Objective

Add the first UI shell step for spawn workflow: background right-click opens menu, template click opens read-only settings panel, and no preview/spawn occurs yet.

## Scope

- preserve runtime controls and key mappings
- add spawn template list (Sun/planets + Black Hole placeholder)
- add background-only right-click spawn menu opening
- add menu hover + scroll + item click handling
- add read-only settings panel shell with derived volume/density
- add `Set` and `Cancel` button behaviors for PR28 shell
- ensure `Set` does not create preview/spawn
- ensure `Cancel` closes panel and discards draft
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no source-data mutation in `solar_system_data.py`
- no grid warp/trail/focus/camera-preset behavior changes
- no editable text fields
- no placement preview
- no body spawn or physics insertion
- no black hole physics / GR / geodesic behavior
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/spawn_workflow.py`
- `src/universe/rendering.py`
- `src/universe/selection.py` (only if needed)
- `tests/test_spawn_workflow.py`
- `tests/test_overlay_controls.py` (only if needed)
- `tests/test_selection.py` (only if needed)
- `README.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/architecture.md`
- `agent/task.md`
- `harness/scenarios/`

## Verification

- run `bash -n scripts/check.sh scripts/test.sh scripts/inspect-diff.sh scripts/rollback.sh`
- run `./scripts/test.sh`
- run `./scripts/check.sh`
- run `./scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- verify right-click background opens spawn menu
- verify template click opens settings shell (no preview, no spawn)
- verify menu wheel scroll does not zoom camera
- verify existing controls remain compatible

## Suggested Next PR

`PR29: Add editable spawn settings fields`
