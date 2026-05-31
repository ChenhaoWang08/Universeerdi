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
The active work is now `PR11`, which adds render scale policy and minimum/maximum visible radius clamps.

## PR11 Scope

`PR11` should:

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- add explicit physical-to-render scale mapping
- map physical positions to render/world coordinates through a clear policy
- map physical radii to visible radii with min/max clamping
- keep selection hit testing compatible with rendered radius
- add deterministic non-window tests for render-scale behavior

## PR11 Non-Goals

`PR11` must not include:

- Newtonian equation changes
- new physics integrators
- physical mass/position/velocity/radius mutations for visual tuning
- long-term solar-system stability guarantees
- Lorentz factor or relativity display
- mass-based grid distortion
- fullscreen mode
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
