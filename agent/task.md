# PR15: Convert overlay toggles into checkbox-style controls

## Objective

Convert overlay Labels/Trails toggles into checkbox-style controls while preserving existing behavior.

## Scope

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- render Labels toggle as checkbox-style text (for example `[X] Labels`)
- render Trails toggle as checkbox-style text (for example `[ ] Trails`)
- preserve existing toggle semantics and click hitbox behavior
- preserve overlay click priority over selection and camera drag
- keep time/display status visible in overlay
- add non-window tests for checkbox label logic and overlay compatibility

## Non-Goals

- no Newtonian equation changes
- no new physics integrator
- no simulation-mode default changes
- no body editing or dragging
- no save/load settings
- no UI framework
- no Lorentz factor
- no grid distortion
- no ephemeris/JPL integration
- no networking or external API runtime behavior

## Allowed Files

- `src/main.py`
- `src/universe/overlay_controls.py`
- `src/universe/rendering.py`
- `src/universe/checkbox_controls.py` (only if needed)
- `tests/test_overlay_controls.py`
- `tests/test_display_modes.py` (only if needed)
- `tests/test_time_controls.py` (only if needed)
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
- verify checkbox controls render in overlay
- verify labels/trails toggles still work
- verify time/display status remains visible

## Suggested Next PR

`PR16: Add Lorentz factor display as an optional computed metric`
