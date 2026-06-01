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
PR16 Lorentz gamma is a read-only inspector metric and does not alter Newtonian stepping or physics state.
PR17 mode/preset controls switch active simulation view and render policy without changing Newtonian equations or source dataset values.
PR18 solar mass multiplier and absorption are runtime experiment controls layered on stepping/state flow and do not change Newtonian equation definitions or source constants.
PR19 camera view presets switch camera bounds/zoom behavior only and do not change simulation state, source constants, or Newtonian equations.
PR20 fixed physics substeps split solar-system frame dt and run absorption per slice without replacing the integrator or changing Newtonian equations.
PR21 focus-body camera mode follows selected render bodies and does not alter simulation stepping or source constants.
PR22 distance scale ruler and preset explanations are informational render annotations and do not alter simulation or physics state.
PR23 trail reset/length controls adjust trail-history storage and rendering only and do not alter simulation or physics state.
PR24 mass-based grid distortion affects grid rendering only and does not alter simulation, source data, or Newtonian force/acceleration updates.
PR25 constrains PR24 distortion with relative-mass hierarchy and visibility thresholds so overview visuals remain Sun-dominant without altering simulation or physics state.
PR26 adds zoom-aware local warp visibility with screen-space caps so small bodies can show close-up local effects while keeping PR25 overview suppression intact.
