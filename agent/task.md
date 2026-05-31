# PR20: Add physics substeps for high-gravity stability

## Objective

Add fixed physics substeps for `solar_system` stepping so high-gravity experiments are more stable and less likely to skip Sun absorption in one large frame step.

## Scope

- add pure substep state model with fixed values
- add runtime controls to increase/decrease substeps
- split `solar_system` frame `dt` into `N` substeps
- apply existing absorption rule after each substep
- keep controlled demo mode behavior unchanged
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no adaptive timestep
- no source data mutation in `solar_system_data.py`
- no solar mass multiplier semantic changes
- no absorption radius/collision-model changes
- no focus-body camera follow
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/physics_substeps.py`
- `src/universe/solar_system_simulation.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `tests/test_physics_substeps.py`
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

## Verification

- run `bash -n scripts/check.sh scripts/test.sh scripts/inspect-diff.sh scripts/rollback.sh`
- run `./scripts/test.sh`
- run `./scripts/check.sh`
- run `./scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- verify viewer launches
- verify `=` increases substeps and `-` decreases substeps
- verify overlay shows `Substeps: N`
- verify no traceback while switching mode/scale/camera/solar-mass/time/fullscreen controls

## Suggested Next PR

`PR21: Add focus body camera mode`
