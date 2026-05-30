# Architecture Overview

The planned architecture for `universeerdi` is intentionally modular:

- app loop: owns startup, event loop, timing, and shutdown
- input: translates mouse and keyboard actions into camera or UI actions
- camera: owns world-to-screen transforms, pan, and zoom
- grid: computes zoom-aware grid spacing and visible grid lines
- body model: stores physical celestial-body data in SI units plus display-only visual metadata
- simulation layout: maps named bodies into placeholder world positions for the viewer without implying real orbital motion
- controlled demo simulation: owns PR5 demo-only SI states and steps them through PR4 Newtonian physics
- rendering: draws background, grid, bodies, and later UI layers
- future solar-system runtime physics: will later connect real dataset motion with careful validation
- future UI: will later own real checkbox behavior and time controls

Physical scale and visual scale must remain separate so realistic distances do not make the scene unusable.
`visual_radius_px` exists only for visibility.
`mean_radius_m` and `mean_orbital_radius_m` are physical quantities and must not be used directly as screen pixels.
PR5 controlled demo physics is intentionally separate from real solar-system dataset motion.
