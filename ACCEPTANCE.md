# PR5 Acceptance Criteria

`PR5` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- a controlled demo simulation path exists
- the controlled demo uses PR4 Newtonian physics stepping (`step_bodies` or equivalent)
- demo physics state and render coordinates remain separated
- demo moving bodies are clearly separated from real solar-system data constants
- no hardcoded circular orbit animation is used for motion
- no real ephemeris, JPL Horizons runtime integration, or network data fetch is added
- no Lorentz factor, trails, labels, grid distortion, real checkbox behavior, or fullscreen behavior is added
- camera drag, mouse-wheel zoom, and dynamic grid remain available in the viewer runtime
- tests verify demo logic without opening a window
- existing physics tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
