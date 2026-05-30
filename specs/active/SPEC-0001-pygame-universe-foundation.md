# SPEC-0001: Pygame Universe Foundation

## Status

Active

## Objective

Create a minimal runnable Pygame viewer foundation for `universeerdi` without implementing real solar-system data or real physics.

## Scope

`PR2` should include:

- a Pygame app entry point
- a resizable non-fullscreen window
- clean quit handling
- a camera model
- background drag panning
- mouse wheel zoom
- a dark gray background
- a light gray or white dynamic grid
- zoom-adaptive grid spacing
- placeholder celestial bodies such as Sun, Earth, and Mars
- a basic top-left UI placeholder area
- non-window tests for camera and grid logic

## Non-Goals

`PR2` must not include:

- real solar-system data sets
- real masses, distances, or orbital periods
- Newtonian gravity or N-body simulation
- relativistic display logic
- Lorentz factor calculations
- geodesic fitting
- mass-based grid distortion
- trail rendering
- fully functional UI controls
- fullscreen mode
- networking, deployment, or external service hooks

## Design Constraints

- Keep physical scale separate from visual scale.
- Do not hardcode orbit paths as fake physics.
- Keep camera and grid logic testable without opening a window.
- Keep the initial viewer small and easy to review.

## Acceptance Summary

The viewer foundation passes when it launches through `python -m src.main`, opens a resizable window, supports drag pan and wheel zoom, shows a dynamic grid on a dark background, shows at least three placeholder bodies, and stays within scope.

## Deferred Work

The following are explicitly deferred to later phases:

- real solar-system body parameters
- Newtonian N-body force integration
- time controls beyond a simple foundation
- labels, trails, and richer UI behavior
- relativistic or grid-distortion effects
