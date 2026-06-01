# Roadmap

## Phase A: Viewer Foundation

- Pygame window
- camera pan
- zoom
- dynamic grid
- placeholder celestial bodies
- UI placeholder

## Phase B: Solar System Data Foundation

- real celestial body names
- mass
- radius
- distance
- initial velocity
- rotation period
- orbital period
- unit system

## Phase C: Newtonian N-body Simulation

- body-body force
- velocity update
- position update
- time step
- numerical stability
- completed in recent PRs: solar_system mode using existing dataset initialization and Newtonian stepping

## Phase D: Rendering and UX

- dashed trails
- planet labels
- zoom-aware visible radius
- planet colors
- time controls
- pause and resume
- fullscreen toggle while preserving resizable window mode
- checkbox-style overlay controls for labels and trails
- runtime simulation mode selection and render-scale presets
- solar mass multiplier experiment with absorption
- camera zoom range controls and view presets
- fixed physics substeps for high-gravity stability
- focus-body camera mode
- current PR focus: distance scale ruler and preset explanations

## Phase E: Relativistic / Visual Effects

- Lorentz factor display
- mass-based grid distortion
- geodesic-like visual approximation
