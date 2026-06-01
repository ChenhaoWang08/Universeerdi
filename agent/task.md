# PR22: Add distance scale ruler and preset explanations

## Objective

Add an informational solar-system distance scale ruler and short render-scale preset explanations.

## Scope

- add a pure scale-ruler helper
- support deterministic distance labels in m/km/AU
- add preset explanation helper text for readable/realistic/overview
- show ruler + explanation in bottom-left for `solar_system` mode
- keep `controlled_demo` without solar-system ruler
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no solar mass / absorption / substep behavior changes
- no focus camera or camera preset behavior changes
- no source data mutation in `solar_system_data.py`
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `.gitignore` (local generated artifact ignore rules only if needed)
- `src/main.py`
- `src/universe/scale_ruler.py`
- `src/universe/render_scale_presets.py`
- `src/universe/rendering.py`
- `tests/test_scale_ruler.py`
- `tests/test_render_scale_presets.py`
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
- switch to `solar_system` mode and confirm bottom-left ruler appears
- cycle presets with `V` and confirm scale-note text updates
- switch back to `controlled_demo` and confirm no solar-system ruler

## Suggested Next PR

`PR23: Add trail reset and trail length controls`
