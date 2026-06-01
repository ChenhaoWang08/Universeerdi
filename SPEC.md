# Project Specification

## Final Vision

`universeerdi` should become a Python + Pygame 2D top-down solar-system simulator with interactive camera controls, real solar-system data, Newtonian N-body motion, and later visual or relativistic display features.

## Current Phase

`PR1` established the workflow control system.
`PR2` established the runnable viewer foundation.
`PR3` added the real solar-system body data foundation and fixed viewer stabilization issues.
`PR4` added a pure Newtonian N-body physics foundation.
`PR5` connected the PR4 physics foundation to a controlled demo simulation path.
`PR6` added visual trails and labels behind feature flags.
`PR7` added simple clickable in-window toggle controls for those overlay flags.
`PR8` added a basic read-only demo body selection inspector.
`PR9` added a `solar_system` simulation mode using existing dataset values and Newtonian stepping.
`PR10` added runtime pause/resume, bounded time scale, and dt clamp controls.
`PR11` added render scale policy and minimum/maximum visible radius clamps.
`PR12` extended the read-only inspector for real solar-system body fields.
`PR13` improved trail readability with dashed body-colored paths.
`PR14` added fullscreen toggle while preserving resizable windowed mode.
`PR15` converted overlay toggles to checkbox-style controls.
`PR16` added Lorentz factor as a read-only display metric.
`PR17` added runtime mode selection and render-scale presets.
`PR18` added solar mass multiplier experiment with absorption.
`PR19` added camera zoom range controls and view presets.
`PR20` added fixed physics substeps for high-gravity stability.
`PR21` added focus-body camera mode.
`PR22` added distance scale ruler and preset explanations.
`PR23` added trail reset and trail length controls.
`PR24` added mass-based grid distortion as a visual-only effect.
`PR25` constrained grid warp by relative mass hierarchy.
`PR26` added zoom-aware local grid warp visibility.
`PR27` smoothed field-based grid warp rendering.
The active work is now `PR28`, which adds right-click spawn menu and settings panel shell.

## PR28 Scope

`PR28` should:

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- preserve all existing key mappings and runtime controls
- open spawn menu on background-only right click
- show scrollable spawn templates including Sun, planets, and Black Hole placeholder
- highlight hovered menu row
- open read-only settings panel shell after template click
- show read-only defaults and derived values in the panel
- show `Set` and `Cancel` buttons
- ensure `Set` does not create preview or spawn body in this PR
- ensure `Cancel` closes panel and discards draft
- keep the workflow shell isolated to UI/input/rendering state
- preserve mode/scale/overlay/time/fullscreen/selection/camera/focus compatibility
- preserve trail controls from PR23 unchanged
- add deterministic non-window tests for spawn menu/panel behavior

## PR28 Non-Goals

`PR28` must not include:

- Newtonian equation changes
- mutation of `solar_system_data.py` constants
- solar mass multiplier semantic changes
- absorption behavior changes
- physics substeps behavior changes
- focus camera behavior changes
- camera view preset behavior changes
- render-scale preset behavior changes
- editable text fields
- placement preview
- actual body spawning or physics insertion
- black hole physics/GR/geodesic/lensing behaviors
- geodesic/GR/lensing simulation
- high-precision ephemeris/JPL integrations
- networking or external services

## Core Principles

- Physical scale and visual scale must remain separate.
- Real body constants must use SI units internally.
- `visual_radius_px` is for display only and must not be treated as physical radius.
- `mean_orbital_radius_m` must not be treated as screen pixels.
- `solar_system` mode from PR9 remains deterministic initialization plus Newtonian stepping, not a precision ephemeris model.
- `PR10` time controls affect stepping cadence only and do not modify Newtonian equations.
- `PR11` keeps SI physics state unchanged and applies display-only render scale mapping.
- `PR12` inspector is read-only and displays local dataset fields plus runtime physics values.
- `PR13` trails visualize prior rendered positions only and do not affect simulation state.
- `PR14` fullscreen/windowed toggles only change display mode and do not affect simulation state.
- `PR15` checkbox-style overlay controls are display/input polish only and do not alter physics or simulation state.
- `PR16` Lorentz gamma is a special-relativity display metric and is not used by Newtonian simulation.
- `PR17` runtime mode/scale controls affect active view/state wiring only and do not alter Newtonian equations or source dataset constants.
- `PR18` runtime Sun mass multiplier and absorption remain experimental and do not alter Newtonian equation definitions or source constants.
- `PR19` camera view presets and reset controls affect camera/rendering state only and do not alter physics state, source data, or PR18 experiment behavior.
- `PR20` fixed physics substeps split frame dt into multiple Newtonian slices in solar-system mode and apply absorption after each slice without changing equations or replacing the integrator.
- `PR21` focus camera follows selected body in rendering space only and does not alter physics state, source data, or PR18/PR20 stepping semantics.
- `PR22` distance ruler and preset explanations are UI-only annotations and do not alter camera state, physics, simulation stepping, or source data.
- `PR23` trail reset/length controls affect trail history storage and rendering only and do not alter physics, simulation state, source data, camera, or focus.
- `PR24` mass-based grid distortion is a visual metaphor in grid rendering only; it does not alter body motion, forces, or Newtonian equations.
- `PR25` constrains PR24 grid warp with relative mass hierarchy so low-mass planets do not appear Sun-like in overview visuals.
- `PR26` adds zoom-aware local visibility for low-mass bodies while keeping PR25 overview suppression and Sun-dominant hierarchy.
- `PR27` smooths warp field continuity with smoothstep falloff, zoom fade, soft-core distance, and top-K source limiting while remaining visual-only.
- `PR28` introduces spawn workflow UI shell only: right-click menu plus read-only settings panel with no preview/spawn side effects.
