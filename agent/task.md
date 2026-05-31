# PR16: Add Lorentz factor display as an optional computed metric

## Objective

Add Lorentz factor as a read-only computed display metric for selected bodies.

## Scope

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- add pure `relativity.py` helper with Lorentz gamma computation
- display Lorentz gamma in inspector for selected bodies
- keep Lorentz as display-only metric (no physics stepping changes)
- keep existing overlay/selection/time-control/fullscreen compatibility
- add non-window tests for Lorentz helper and inspector field output

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no feed-back of Lorentz gamma into motion
- no special-relativity dynamics
- no general relativity/geodesic/spacetime-curvature simulation
- no mass-based grid distortion
- no save/load settings
- no UI framework
- no ephemeris/JPL integration
- no networking or external API runtime behavior

## Allowed Files

- `src/universe/relativity.py`
- `src/universe/inspector.py`
- `src/universe/rendering.py` (only if needed)
- `src/main.py` (only if needed)
- `tests/test_relativity.py`
- `tests/test_inspector.py`
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
- verify selected-body inspector shows Lorentz gamma
- verify no traceback during normal startup/close smoke flow

## Suggested Next PR

`PR17: Add mass-based grid distortion visual effect`
