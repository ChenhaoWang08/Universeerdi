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
The active work is now `PR10`, which adds runtime pause/resume, bounded time scale, and dt clamp controls.

## PR10 Scope

`PR10` should:

- keep `controlled_demo` mode working
- keep `solar_system` mode working
- add runtime pause/resume controls
- add bounded time scale controls
- clamp frame dt before simulation stepping
- show running/paused state and scale in overlay
- add deterministic non-window tests for time-control behavior

## PR10 Non-Goals

`PR10` must not include:

- Newtonian equation changes
- new physics integrators
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
