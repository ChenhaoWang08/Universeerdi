# PR3 Acceptance Criteria

`PR3` is accepted only if all of the following are true:

- `python3 -m src.main` is the documented primary launch command
- stale mandatory `python -m src.main` references are fixed
- the viewer launches with `python3 -m src.main`
- the window remains resizable and non-fullscreen
- wheel zoom no longer has a double-application risk
- a solar-system body data model exists
- the dataset includes the Sun plus Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune
- SI units are used internally for mass, radius, distance, and periods
- physical scale and visual scale remain separate
- viewer layout positions remain placeholder display values instead of real orbital simulation
- `scripts/check.sh` passes
- tests verify dataset integrity without opening a window
- `python3 -m pytest tests` passes
- the viewer still shows the dark gray background, dynamic grid, and visible bodies
- no Newtonian N-body physics is implemented yet
- no hardcoded real orbital motion is implemented
- no Lorentz factor or grid distortion is implemented
- no network access, secrets, or external APIs are added
