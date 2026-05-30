# PR6 Acceptance Criteria

`PR6` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- controlled demo simulation remains available
- optional trail rendering exists behind a feature flag
- optional label rendering exists behind a feature flag
- trail/label rendering does not change Newtonian physics equations
- no hardcoded circular orbit animation is introduced
- no real ephemeris, runtime network data fetch, or external API integration is added
- no Lorentz factor, grid distortion, fullscreen, or complex UI mode selector is added
- camera drag, mouse-wheel zoom, and dynamic grid remain available
- tests verify trail/label helper behavior without opening a window
- existing physics and demo tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
