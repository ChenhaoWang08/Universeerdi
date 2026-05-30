# Project Specification

## Final Vision

`universeerdi` should become a Python + Pygame 2D top-down solar-system simulator with interactive camera controls, real solar-system data, Newtonian N-body motion, and later visual or relativistic display features.

## Current Phase

`PR1` established the workflow control system.
`PR2` established the runnable viewer foundation.
`PR3` added the real solar-system body data foundation and fixed PR2 stabilization issues.
The active work is now `PR4`, which introduces a pure Newtonian N-body physics foundation while keeping real orbital behavior out of scope.

## PR4 Scope

`PR4` should:

- implement pure, testable Newtonian pairwise gravitational acceleration
- implement deterministic N-body net acceleration summation
- implement velocity and position updates with a documented timestep method
- use semi-implicit Euler integration for the step foundation
- keep physics state in SI units and separate from screen-space render state
- keep viewer behavior stable without wiring full real-orbit runtime motion
- add deterministic non-window tests for physics behavior and safety

## PR4 Non-Goals

`PR4` must not include:

- stable real solar-system orbit tuning
- real orbital motion driven by ephemeris inputs
- hardcoded circular orbit playback
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
