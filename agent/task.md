# PR3: Add solar-system body data model and fix PR2 stabilization issues

## Objective

Add a real solar-system body data foundation for `universeerdi` and fix the remaining PR2 stabilization issues.

## Scope

- make `python3 -m src.main` the documented primary launch command
- treat `python -m src.main` as an alternative only when `python` resolves to Python 3
- remove the wheel zoom double-application risk
- add a `CelestialBody`-style data model with SI fields
- add the Sun and eight planets with real baseline constants
- keep visual display fields separate from physical fields
- keep placeholder viewer positions separate from physical orbital radius
- integrate the real data model into the existing placeholder viewer layout when simple
- add deterministic non-window tests for body data, units, and placeholder integration

## Non-Goals

- no Newtonian N-body gravity
- no real orbital motion driven by the data model
- no relativity
- no Lorentz factor
- no geodesic fitting
- no mass-based grid distortion
- no planet trail rendering
- no real checkbox behavior
- no fullscreen mode
- no save or load
- no networking
- no deployment

## Required Design

- launch with `python3 -m src.main`
- use a resizable non-fullscreen window
- allow camera pan by dragging the background, not planets
- use mouse wheel zoom with scroll up zooming out and scroll down zooming in
- render a dark gray background
- render a light gray or white dynamic grid
- keep grid density controlled as zoom changes
- store mass, radius, distance, and periods in SI units
- keep `visual_radius_px` separate from `mean_radius_m`
- keep `mean_orbital_radius_m` separate from placeholder screen layout
- show visible solar-system bodies using placeholder display positions
- reserve a top-left UI placeholder area for future checkboxes
- keep all PR3 tests non-windowed
- document official NASA or JPL data sources and any fallback reasoning

## Allowed Files

- `README.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `agent/task.md`
- `docs/architecture.md`
- `docs/operating-model.md`
- `docs/data-sources.md`
- `src/universe/body.py`
- `src/universe/solar_system_data.py`
- `src/universe/units.py`
- `src/universe/data_sources.py`
- `src/universe/simulation.py`
- `src/universe/rendering.py`
- `src/universe/physics.py`
- `src/main.py`
- `tests/test_body.py`
- `tests/test_solar_system_data.py`
- `tests/test_units.py`
- `tests/test_simulation.py`
- `tests/test_physics.py`
- `harness/scenarios/`
- `harness/judges/`
- `reviews/REVIEW-0001-pygame-universe-foundation.md`
- `scripts/check.sh`
- `scripts/test.sh`
- `scripts/inspect-diff.sh`

## Forbidden Files

- `.env`
- `.env.*`
- `secrets/`
- deployment files
- `.github/workflows/`
- external API configuration
- binary assets
- unrelated docs
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
- verify the window opens and is resizable
- verify the background is dark gray
- verify the grid is visible and adapts to zoom
- verify dragging the background pans the camera
- verify scroll up zooms out and scroll down zooms in
- verify wheel zoom applies once per wheel tick
- verify visible bodies still appear in the scene
- verify closing the window exits without traceback or a hanging process

## Final Report Format

Use `agent/final-report-template.md` and include:

- Summary
- PR2.5 Fixes
- Files changed
- Commands run
- Test results
- Manual verification notes
- Data Model Summary
- Acceptance Check
- Risks
- Unresolved issues
- Suggested next PR

## Suggested Next PR

`PR4: Add initial Newtonian N-body physics foundation`
