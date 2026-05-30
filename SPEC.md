# Project Specification

## Final Vision

`universeerdi` should become a Python + Pygame 2D top-down solar-system simulator with interactive camera controls, real solar-system data, Newtonian N-body motion, and later visual or relativistic display features.

## Current Phase

`PR1` established the workflow control system.
`PR2` established the runnable viewer foundation.
`PR3` added the real solar-system body data foundation and fixed viewer stabilization issues.
`PR4` added a pure Newtonian N-body physics foundation.
The active work is now `PR5`, which connects the PR4 physics foundation to a controlled demo simulation path.

## PR5 Scope

`PR5` should:

- add a controlled demo simulation mode that uses PR4 Newtonian physics stepping
- keep demo physics states in SI units and separate from screen-space render coordinates
- keep real solar-system dataset constants separate from demo moving bodies
- optionally render moving demo bodies in the viewer runtime
- keep camera drag, mouse-wheel zoom, and dynamic grid behavior stable
- add deterministic non-window tests for controlled demo setup and stepping behavior

## PR5 Non-Goals

`PR5` must not include:

- stable real solar-system orbit tuning
- real ephemeris inputs or JPL Horizons runtime integration
- hardcoded circular orbit animation
- Kepler solver features
- Lorentz factor or relativity display
- geodesic fitting
- mass-based grid distortion
- trail rendering or planet labels
- real checkbox behavior
- fullscreen mode
- save or load features
- networking, deployment, or external services

## Core Principles

- Physical scale and visual scale must remain separate.
- Real body constants must use SI units internally.
- `visual_radius_px` is for display only and must not be treated as physical radius.
- `mean_orbital_radius_m` must not be treated as screen pixels.
- Controlled demo simulation is for verification only and is not a claim of real solar-system stability.
