# PR29: Add editable spawn settings fields

## Objective

Build on PR28 spawn workflow shell by making settings fields editable and validating draft values on `Set`, while still forbidding preview/spawn.

## Scope

- preserve PR28 spawn menu and panel shell flow
- make Name/Mass/Radius/Velocity X/Velocity Y/Color RGB editable
- support cursor-based single-line editing and select-all replacement
- validate numeric and RGB fields on `Set`
- keep Volume/Density derived read-only
- show valid/error note after validation
- keep `Set`/`Cancel` behaviors deterministic and testable
- keep no-preview/no-spawn policy

## Non-Goals

- no Newtonian equation changes
- no source-data mutation in `solar_system_data.py`
- no grid warp/trail/focus/camera-preset behavior changes
- no placement preview
- no body spawn or physics insertion
- no black hole physics / GR / geodesic behavior
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/spawn_workflow.py`
- `src/universe/rendering.py`
- `tests/test_spawn_workflow.py`
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
- verify text editing in settings panel fields
- verify valid/invalid Set notes
- verify no preview/spawn side effects
- verify existing controls remain compatible

## Suggested Next PR

`PR30: Add spawn placement preview after valid Set`
