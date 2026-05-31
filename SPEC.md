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
The active work is now `PR9`, which adds a `solar_system` simulation mode using existing dataset values and Newtonian stepping.

## PR9 Scope

`PR9` should:

- keep `controlled_demo` mode working
- add `solar_system` simulation mode
- build `PhysicsBodyState` values from existing solar-system dataset fields
- use deterministic SI initial conditions (Sun at origin, planets on +x, +y tangential velocity estimate)
- step runtime motion through existing `step_bodies(...)`
- keep selection, overlays, and inspector compatible with the new mode
- add deterministic non-window tests for solar-system mode construction and stepping

## PR9 Non-Goals

`PR9` must not include:

- high-precision ephemeris initialization
- JPL Horizons runtime integration
- hardcoded per-frame circular orbit animation
- Newtonian equation changes
- long-term solar-system stability guarantees
- Lorentz factor or relativity display
- mass-based grid distortion
- fullscreen mode
- time controls
- networking or external services

## Core Principles

- Physical scale and visual scale must remain separate.
- Real body constants must use SI units internally.
- `visual_radius_px` is for display only and must not be treated as physical radius.
- `mean_orbital_radius_m` must not be treated as screen pixels.
- `solar_system` mode in PR9 is a deterministic initialization plus Newtonian stepping, not a precision ephemeris model.
