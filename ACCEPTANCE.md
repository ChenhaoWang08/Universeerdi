# PR7 Acceptance Criteria

`PR7` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- controlled demo simulation remains available
- clickable `Labels` toggle exists in the top-left overlay area
- clickable `Trails` toggle exists in the top-left overlay area
- clicking Labels updates label rendering state
- clicking Trails updates trail rendering state
- clicking overlay controls is consumed and does not start camera drag
- camera drag and mouse-wheel zoom still work outside control interactions
- toggles affect rendering visibility only and do not modify physics equations
- no hardcoded circular orbit animation is introduced
- no real ephemeris, runtime network fetch, or external API integration is added
- no Lorentz factor, grid distortion, fullscreen, or UI framework is added
- tests verify overlay control logic without opening a window
- existing physics/demo tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
