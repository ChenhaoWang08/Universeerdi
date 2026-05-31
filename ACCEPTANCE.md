# PR8 Acceptance Criteria

`PR8` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- controlled demo simulation remains available
- clicking a rendered demo body can select it
- selection renders a visible highlight indicator
- a read-only inspector panel displays selected body fields (name, mass, position, velocity)
- overlay control clicks are consumed before body selection
- body selection click is consumed before camera drag start
- camera drag and mouse-wheel zoom still work on non-UI background interactions
- selection and inspector behavior does not change Newtonian equations
- no body dragging or editing is introduced
- no hardcoded circular orbit animation is introduced
- no real ephemeris, runtime network fetch, or external API integration is added
- no Lorentz factor, grid distortion, fullscreen, or UI framework is added
- tests verify selection/inspector logic without opening a window
- existing physics/demo/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
