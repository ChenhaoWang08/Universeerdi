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
The active work is now `PR8`, which adds a basic read-only demo body selection inspector.

## PR8 Scope

`PR8` should:

- support selecting a rendered demo body by click hit testing
- keep selection state in runtime/rendering control paths only
- render a read-only inspector panel for the selected demo body
- render a visual selection indicator for the selected body
- preserve overlay toggle priority and camera input behavior
- add deterministic non-window tests for selection logic and inspector formatting

## PR8 Non-Goals

`PR8` must not include:

- Newtonian equation changes
- body dragging or body editing
- stable real solar-system orbit tuning
- real ephemeris inputs or JPL Horizons runtime integration
- hardcoded circular orbit animation
- Lorentz factor or relativity display
- mass-based grid distortion
- fullscreen mode
- complex UI framework
- networking, deployment, or external services

## Core Principles

- Physical scale and visual scale must remain separate.
- Real body constants must use SI units internally.
- `visual_radius_px` is for display only and must not be treated as physical radius.
- `mean_orbital_radius_m` must not be treated as screen pixels.
- Controlled demo simulation is for verification only and is not a claim of real solar-system stability.
