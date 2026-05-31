# Architecture Overview

The planned architecture for `universeerdi` is intentionally modular:

- app loop: owns startup, event loop, timing, and shutdown
- input: translates mouse and keyboard actions into camera or UI actions
- camera: owns world-to-screen transforms, pan, and zoom
- grid: computes zoom-aware grid spacing and visible grid lines
- body model: stores physical celestial-body data in SI units plus display-only visual metadata
- simulation layout: maps named bodies into placeholder world positions for the viewer without implying real orbital motion
- controlled demo simulation: owns PR5 demo-only SI states and steps them through PR4 Newtonian physics
- rendering: draws background, grid, bodies, overlays, selection highlights, and inspector panel
- overlay controls: manages top-left hitboxes and runtime visibility toggles for labels/trails
- selection helpers: handle render-space body hit testing and inspector text formatting without Pygame dependencies
- future solar-system runtime physics: will later connect real dataset motion with careful validation

Physical scale and visual scale must remain separate so realistic distances do not make the scene unusable.
`visual_radius_px` exists only for visibility.
`mean_radius_m` and `mean_orbital_radius_m` are physical quantities and must not be used directly as screen pixels.
Controlled demo physics is intentionally separate from real solar-system dataset motion.
