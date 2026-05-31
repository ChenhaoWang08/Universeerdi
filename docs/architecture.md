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
- render scale policy: maps physical meters/radii into display-oriented render/world coordinates and visible radii
- rendering: draws background, grid, bodies, overlays, selection highlights, and inspector panel
- trails helpers: build bounded render-history and dashed polyline geometry for rendering-only trail visualization
- display mode helpers: manage fullscreen/windowed runtime state separate from simulation state
- overlay controls: manages top-left hitboxes and runtime visibility toggles for labels/trails
- selection helpers: handle render-space body hit testing and inspector text formatting without Pygame dependencies
- inspector helpers: assemble read-only body-inspector lines from runtime physics values and local dataset metadata

Physical scale and visual scale must remain separate so realistic distances do not make the scene unusable.
`visual_radius_px` exists only for visibility.
`mean_radius_m` and `mean_orbital_radius_m` are physical quantities and must not be used directly as screen pixels.
PR9 solar-system mode uses deterministic initialization and does not provide precision ephemeris guarantees.
PR10 time controls change stepping cadence only and do not modify Newtonian equations.
PR11 keeps physics in SI units and applies display-only position/radius mapping for readability.
PR12 inspector remains display-only and shows local dataset fields without runtime network fetching.
PR13 keeps trails rendering-only and does not alter simulation state or physics equations.
PR14 fullscreen toggle changes display mode only and does not alter simulation state or physics equations.
PR15 checkbox-style overlay controls remain display/input polish only and do not alter simulation state or physics equations.
