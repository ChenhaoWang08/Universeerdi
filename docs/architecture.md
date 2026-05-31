# Architecture Overview

The planned architecture for `universeerdi` is intentionally modular:

- app loop: owns startup, event loop, timing, and shutdown
- input: translates mouse and keyboard actions into camera or UI actions
- camera: owns world-to-screen transforms, pan, and zoom
- grid: computes zoom-aware grid spacing and visible grid lines
- body model: stores physical celestial-body data in SI units plus display-only visual metadata
- controlled demo simulation: owns PR5 demo-only SI states and steps them through PR4 Newtonian physics
- solar-system simulation: builds SI initial states from existing dataset values and advances them through PR4 Newtonian stepping
- time controls: owns pause/resume state, bounded time scale, and dt clamp policy for runtime stepping cadence
- rendering: draws background, grid, bodies, overlays, selection highlights, and inspector panel
- overlay controls: manages top-left hitboxes and runtime visibility toggles for labels/trails
- selection helpers: handle render-space body hit testing and inspector text formatting without Pygame dependencies

Physical scale and visual scale must remain separate so realistic distances do not make the scene unusable.
`visual_radius_px` exists only for visibility.
`mean_radius_m` and `mean_orbital_radius_m` are physical quantities and must not be used directly as screen pixels.
PR9 solar-system mode uses deterministic initialization and does not provide precision ephemeris guarantees.
PR10 time controls change stepping cadence only and do not modify Newtonian equations.
