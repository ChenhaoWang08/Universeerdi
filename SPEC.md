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
The active work is now `PR16`, which adds Lorentz factor as a read-only display metric.

## PR16 Scope

`PR16` should:

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- add a pure Lorentz helper with `gamma = 1 / sqrt(1 - v^2 / c^2)`
- compute Lorentz gamma from runtime velocity for selected inspector body
- render Lorentz gamma as read-only inspector text
- preserve camera/overlay/labels/trails/selection/inspector/time-control compatibility
- keep this as display-only metric work (no simulation or physics behavior change)
- add deterministic non-window tests for Lorentz helper and inspector integration

## PR16 Non-Goals

`PR16` must not include:

- Newtonian equation changes
- new physics integrators
- feeding Lorentz gamma back into dynamics
- special-relativity dynamics, GR, geodesic solving, or spacetime curvature simulation
- physical mass/position/velocity/radius mutations
- long-term solar-system stability guarantees
- mass-based grid distortion
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
