# PR5: Connect physics foundation to a controlled demo simulation

## Objective

Connect the PR4 Newtonian physics foundation to a controlled demo simulation path without claiming real solar-system stability.

## Scope

- add a controlled demo simulation mode with demo-only bodies
- keep demo bodies separate from real solar-system constants
- step demo bodies with PR4 physics (`step_bodies`)
- keep physics in SI units and convert to render coordinates only at display boundary
- optionally render demo motion in runtime viewer
- add non-window tests for demo setup and step behavior

## Non-Goals

- no stable real solar-system tuning
- no real ephemeris or JPL Horizons runtime integration
- no hardcoded circular orbit animation
- no Kepler solver
- no Lorentz factor, trails, labels, or grid distortion
- no fullscreen mode, no save/load, no networking

## Required Design

- launch command remains `python3 -m src.main`
- controlled demo behavior is explicitly documented as non-real and verification-only
- camera drag, zoom, and dynamic grid remain available
- automated tests remain non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/simulation.py`
- `src/universe/physics.py` only if bug fix is required
- `src/universe/body.py` only if integration requires it
- `src/universe/rendering.py`
- `src/universe/demo_simulation.py`
- `tests/test_simulation.py`
- `tests/test_physics.py`
- `tests/test_demo_simulation.py`
- `README.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/architecture.md`
- `agent/task.md`
- `harness/scenarios/`
- `harness/judges/`
- `reviews/`

## Forbidden Files

- `.env`
- `.env.*`
- `secrets/`
- deployment files
- `.github/workflows/`
- external API configuration
- binary assets
- credentials
- tokens

## Verification

- run `bash -n scripts/check.sh scripts/test.sh scripts/inspect-diff.sh scripts/rollback.sh`
- run `scripts/check.sh`
- run `scripts/test.sh`
- run `scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- verify window opens and closes cleanly
- verify grid remains visible
- verify camera drag and zoom remain available
- verify demo bodies visibly move in controlled demo mode

## Suggested Next PR

`PR6: Add visual trails and labels behind feature flags without changing physics correctness`
