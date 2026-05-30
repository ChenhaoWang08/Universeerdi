# Project Specification

## Final Vision

`universeerdi` should become a Python + Pygame 2D top-down solar-system simulator with interactive camera controls, real solar-system data, Newtonian N-body motion, and later visual or relativistic display features.

## Current Phase

`PR1` established the workflow control system.
`PR2` established the runnable viewer foundation.
The active work is now `PR3`, which fixes PR2 stabilization issues and adds the real solar-system body data foundation while keeping real physics out of scope.

## PR3 Scope

`PR3` should:

- document `python3 -m src.main` as the primary launch command
- fix wheel zoom so one physical wheel action is handled through one authoritative path
- add an SI-based solar-system body data model
- include the Sun and eight planets with real baseline parameters
- keep rendering visibility fields separate from physical radius and orbital distance
- keep viewer layout positions placeholder and display-oriented
- add deterministic non-window tests for data integrity and units

## PR3 Non-Goals

`PR3` must not include:

- Newtonian N-body gravity
- real orbital motion driven by physical periods
- relativity or Lorentz factor display
- geodesic fitting
- mass-based grid distortion
- trail rendering
- real checkbox behavior
- fullscreen mode
- save or load features
- networking, deployment, or external services

## Core Principles

- Physical scale and visual scale must remain separate.
- Real body constants must use SI units internally.
- `visual_radius_px` is for display only and must not be treated as physical radius.
- `mean_orbital_radius_m` must not be treated as screen pixels.
- Future physics must not hardcode circular orbits as the motion model.
- Real physics is future work and is not part of `PR1`, `PR2`, or `PR3`.
