# PR18: Add solar mass multiplier experiment with absorption

## Objective

Add an experimental runtime Sun gravity multiplier for `solar_system` mode and a simple absorption rule for bodies entering Sun radius.

## Scope

- keep baseline source dataset unchanged
- keep baseline initial velocity policy based on baseline Sun mass
- add runtime Sun gravity multiplier controls in app loop
- apply multiplier only during solar-system stepping
- restore baseline Sun mass in stored simulation state
- absorb non-Sun bodies that enter Sun physical radius
- show experiment status in overlay
- keep behavior deterministic and testable without opening a window

## Non-Goals

- no Newtonian equation changes
- no new integrator
- no mutation of `solar_system_data.py` constants
- no realistic collision/fluid dynamics
- no GR/geodesic/spacetime modeling
- no mass-based grid distortion
- no save/load settings
- no UI framework
- no network/API/JPL integration

## Allowed Files

- `src/main.py`
- `src/universe/solar_mass_experiment.py`
- `src/universe/solar_system_simulation.py`
- `src/universe/rendering.py`
- `src/universe/overlay_controls.py`
- `tests/test_solar_mass_experiment.py`
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
- run `scripts/check.sh`
- run `scripts/test.sh`
- run `scripts/inspect-diff.sh`
- run `python3 -m pytest tests`

## Manual Verification

- run `python3 -m src.main`
- verify viewer launches
- verify Sun gravity controls affect solar-system behavior
- verify absorption and body-count behavior are visible

## Suggested Next PR

`PR19: Add camera zoom range controls / view presets`
