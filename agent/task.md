# PR17: Add simulation mode selector and render-scale presets

## Objective

Add runtime controls so users can switch simulation mode and solar-system render scale without editing source code.

## Scope

- keep `controlled_demo` and `solar_system` both runnable
- add runtime mode toggle (`M`) between `controlled_demo` and `solar_system`
- add runtime preset cycle (`V`) for `readable`, `realistic`, `overview`
- wire preset policy into `solar_system_to_render_bodies(...)`
- show mode and scale status in top-left overlay
- clear selection and trail history on mode switch
- keep all behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no solar mass multiplier
- no absorption/collision experiment
- no grid distortion or geodesic visuals
- no save/load settings
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/simulation_modes.py`
- `src/universe/render_scale_presets.py`
- `src/universe/solar_system_simulation.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `tests/test_simulation_modes.py`
- `tests/test_render_scale_presets.py`
- `tests/test_solar_system_simulation.py`
- `tests/test_render_scale.py`
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
- run `scripts/check.sh`
- run `scripts/test.sh`
- run `scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- verify viewer launches
- verify `M` toggles mode
- verify `V` cycles scale preset
- verify overlay shows mode + scale

## Suggested Next PR

`PR18: Add solar mass multiplier experiment with absorption`
