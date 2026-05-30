# Acceptance Judge

Judge `PR7` against `ACCEPTANCE.md`.

Pass only if:

- Labels and Trails clickable toggles exist
- clicking toggles updates overlay visibility state
- toggle clicks are consumed before camera drag start
- overlay controls remain rendering/runtime-only and do not change physics equations
- no hardcoded circular-orbit animation was introduced
- no ephemeris, runtime network data fetch, or external API integration was introduced
- no Lorentz/grid-distortion/fullscreen/UI-framework scope creep was introduced
- all listed acceptance checks pass
