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
The active work is now `PR7`, which adds simple clickable in-window toggle controls for those overlay flags.

## PR7 Scope

`PR7` should:

- add simple, clickable top-left controls for `Labels` and `Trails`
- let users toggle overlay visibility during runtime
- keep overlay state in rendering/runtime control layers only
- keep simulation correctness and Newtonian physics unchanged
- preserve camera drag, mouse-wheel zoom, and grid behavior
- add deterministic non-window tests for overlay control logic

## PR7 Non-Goals

`PR7` must not include:

- Newtonian equation changes
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
