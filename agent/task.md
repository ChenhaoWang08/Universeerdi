# PR27: Smooth field-based grid warp rendering

## Objective

Smooth PR26 grid warp rendering so local/global transitions and multi-source behavior feel continuous.

## Scope

- preserve runtime control:
  - `W` toggle grid distortion
- preserve `G/H/R` controls unchanged
- add smoothstep falloff helpers and smooth zoom fade
- add soft-core source distance handling
- add top-K source influence limiting
- keep local warp visible but smoother at close zoom
- preserve optional effective mass overrides for runtime solar-mass experiment visuals
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no solar mass / absorption / substep semantic changes
- no focus camera / camera preset / render-scale / trail behavior changes
- no source data mutation in `solar_system_data.py`
- no help overlay (deferred to PR28)
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
- verify zoomed-in small bodies can show local warp with smoother transitions
- verify existing controls remain compatible

## Suggested Next PR

`PR28: Add help overlay for controls`
