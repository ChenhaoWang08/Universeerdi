# PR25: Add mass-aware grid warp scaling constraints

## Objective

Constrain PR24 grid warp so low-mass planets do not look Sun-like in overview views.

## Scope

- preserve runtime control:
  - `W` toggle grid distortion
- replace raw log-mass scaling with relative-to-Sun mass scaling
- add visibility threshold and influence-radius scaling policy
- preserve optional effective mass overrides for runtime solar-mass experiment visuals
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no solar mass / absorption / substep semantic changes
- no focus camera / camera preset / render-scale / trail behavior changes
- no source data mutation in `solar_system_data.py`
- no help overlay (deferred to PR26)
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/grid_distortion.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `tests/test_grid_distortion.py`
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

## Verification

- run `bash -n scripts/check.sh scripts/test.sh scripts/inspect-diff.sh scripts/rollback.sh`
- run `./scripts/test.sh`
- run `./scripts/check.sh`
- run `./scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- verify `W` toggles grid warp status and visual effect
- verify overview warp is Sun-dominant and terrestrial planets are visually suppressed
- verify existing controls remain compatible

## Suggested Next PR

`PR26: Add help overlay for controls`
