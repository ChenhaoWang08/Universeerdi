# Acceptance Judge

Judge `PR8` against `ACCEPTANCE.md`.

Pass only if:

- demo body click selection works
- selection highlight and read-only inspector are visible
- inspector content includes required fields
- input priority remains overlay controls > body selection > camera drag
- selection is rendering/runtime-only and does not modify physics equations
- no body dragging or editing was introduced
- no hardcoded circular-orbit animation was introduced
- no ephemeris, runtime network data fetch, or external API integration was introduced
- no Lorentz/grid-distortion/fullscreen/UI-framework scope creep was introduced
- all listed acceptance checks pass
