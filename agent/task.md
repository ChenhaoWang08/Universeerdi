# PR9: Add real solar-system simulation mode using existing body data

## Objective

Add a `solar_system` simulation mode that builds and steps physics states from existing solar-system dataset values.

## Scope

- keep `controlled_demo` mode working
- add `solar_system` mode as a separate runtime path
- build `PhysicsBodyState` entries from real dataset values in SI units
- use deterministic initial conditions (Sun at origin, planets on +x, +y tangential speed estimate)
- step runtime motion via `step_bodies(...)`
- keep overlays, selection, and inspector compatible
- add non-window tests for builder and stepping logic

## Non-Goals

- no high-precision ephemeris integration
- no JPL Horizons runtime integration
- no hardcoded per-frame circular orbit animation
- no Newtonian equation changes
- no long-term stability guarantee claims
- no Lorentz factor
- no grid distortion
- no fullscreen mode
- no time controls

## Required Design

- launch with `python3 -m src.main`
- preserve existing control and render behavior for demo mode
- keep physics state in SI units
- keep data-source objects immutable from simulation builder behavior
- keep automated tests non-windowed

## Allowed Files

- `src/main.py`
- `src/universe/simulation.py`
- `src/universe/demo_simulation.py` only if needed for mode compatibility
- `src/universe/solar_system_simulation.py`
- `src/universe/solar_system_data.py` only if needed for cleaner access
- `src/universe/rendering.py` only if mode compatibility needs it
- `src/universe/selection.py` only if graceful compatibility needs it
- `src/universe/units.py` only if helper/constants additions are needed
- `tests/test_solar_system_simulation.py`
- `tests/test_simulation.py`
- `tests/test_solar_system_data.py`
- `tests/test_demo_simulation.py`
- `README.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/architecture.md`
- `docs/data-sources.md`
- `agent/task.md`
- `harness/scenarios/`
- `harness/judges/`

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
- verify viewer launches
- verify no immediate traceback
- optionally switch to `solar_system` mode and confirm runtime still runs

## Suggested Next PR

`PR10: Add pause, resume, and time scale controls`
