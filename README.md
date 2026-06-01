# universeerdi

`universeerdi` is a Python + Pygame 2D top-down solar-system physics simulator project.

The long-term goal is an interactive viewer and simulation that can support camera pan and zoom, source-backed solar-system data, Newtonian N-body motion, and later visual or relativistic effects.

The current workflow is Spec-first Agent Engineering plus Agentic Harness Engineering.
`PR1` initialized control files and review workflow.
`PR2` implemented the minimal viewer foundation.
`PR3` added the real solar-system body data foundation.
`PR4` added a pure Newtonian N-body physics foundation.
`PR5` connected controlled demo motion to physics stepping.
`PR6` added optional visual trails and labels.
`PR7` added clickable in-window overlay toggles.
`PR8` added a read-only demo body selection inspector.
`PR9` added a `solar_system` simulation mode using existing dataset values.
`PR10` added pause/resume, bounded time scale, and dt clamp controls for simulation stepping.
`PR11` added physical-to-render scale policy and visible radius clamps.
`PR12` extended the read-only inspector for real solar-system fields.
`PR13` improved trail readability with dashed body-colored paths.
`PR14` added fullscreen toggle while preserving resizable windowed mode.
`PR15` converted overlay toggles to checkbox-style controls.
`PR16` added Lorentz factor as a read-only display metric.
`PR17` added runtime simulation mode selection and render-scale presets.
`PR18` added an experimental solar mass multiplier with absorption.
`PR19` added camera zoom range controls and view presets.
`PR20` added fixed physics substeps for high-gravity stability.
`PR21` added focus body camera mode.
`PR22` added distance scale ruler and preset explanations.
`PR23` added trail reset and trail length controls.
`PR24` added mass-based grid distortion as a visual-only effect.
`PR25` constrained grid warp by relative mass hierarchy.
`PR26` added zoom-aware local grid warp visibility.
`PR27` smoothed field-based grid warp rendering.
The current phase is `PR28`, which adds a right-click spawn menu and read-only settings panel shell.

Primary launch command:

```bash
python3 -m src.main
```

Alternative:

```bash
python -m src.main
```

Use the alternative only when `python` resolves to Python 3 on the local machine.

Simulation modes are currently selected by `DEFAULT_SIMULATION_MODE` in [src/main.py](/Users/zhangyixin/Desktop/universeerdi/src/main.py):
- `"controlled_demo"`
- `"solar_system"`

PR9 `solar_system` mode uses deterministic initialization from existing data plus Newtonian stepping.
It does not claim high-precision ephemeris positions or long-term orbital stability guarantees.

PR10 time controls affect simulation stepping frequency only.
PR10 does not change Newtonian physics equations.

PR11 separates physical simulation units from rendering scale.
Physics continues using SI units; rendering applies visual mapping plus minimum/maximum visible radii.

PR12 inspector fields are display-only.
Solar-system inspector values come from local `solar_system_data.py` plus runtime physics state (no live API calls).

PR13 trails are rendering-only and body-colored.
Trail history remains bounded and does not change physics simulation state.

PR14 display controls:
- `F11`: toggle fullscreen/windowed mode
- `Escape`: exits fullscreen first; in windowed mode it keeps existing quit behavior

PR14 display mode changes are rendering/window-only and do not affect physics simulation state.

PR15 overlay controls:
- `[X] Labels` toggles label visibility
- `[X] Trails` toggles trail visibility
- PR15 is UI polish only and does not change physics equations or simulation behavior

PR16 Lorentz metric:
- Inspector displays `Lorentz gamma` computed from current body speed.
- Formula: `gamma = 1 / sqrt(1 - v^2 / c^2)` with `c = 299792458 m/s`.
- This is a special-relativity display metric only.
- It does not change Newtonian stepping, force, acceleration, velocity, or position.
- It is not a general relativity, geodesic, or spacetime-curvature simulation.

PR17 runtime controls:
- `M`: toggle simulation mode between `controlled_demo` and `solar_system`
- `V`: cycle solar-system render-scale preset: `readable -> realistic -> overview`
- Render-scale presets affect display only and do not mutate physics state or source data.

PR18 solar experiment controls:
- `G`: increase runtime Sun gravity multiplier
- `H`: decrease runtime Sun gravity multiplier
- `R`: reset Sun gravity multiplier to `x1.0`
- non-Sun bodies entering the Sun physical radius are absorbed (removed)
- this is an experimental Newtonian visualization feature, not collision fluid dynamics or GR

PR19 camera view controls:
- `B`: cycle camera view preset: `normal -> overview -> close`
- `0`: reset camera to the current view preset defaults
- `Ctrl+0`: reset time scale to `x1.0`
- camera view presets affect camera/rendering state only and do not alter physics state

PR20 physics substep controls:
- `=`: increase solar-system physics substeps
- `-`: decrease solar-system physics substeps
- substeps split frame dt and apply absorption after each slice in `solar_system` mode
- this improves high-gravity experiment stability without changing Newtonian equations

PR21 focus camera controls:
- click to select a body, then press `F` to focus follow
- press `F` again to clear focus
- focus is cleared automatically if the body disappears
- focus is also cleared when manual camera drag begins

PR22 scale interpretation UI:
- in `solar_system` mode, bottom-left shows a distance scale ruler
- ruler uses camera zoom + active render-scale policy mapping
- bottom-left also shows a short scale-note for the active preset
- these annotations are informational only and do not affect camera/physics/simulation state
- `readable` and `overview` remain visualization-friendly modes
- `realistic` is closer to real proportions and can make small bodies harder to see

PR23 trail controls:
- `C`: clear current trail history immediately
- `,`: decrease trail length cap
- `.`: increase trail length cap
- trail controls affect only trail history storage/rendering and do not change physics, simulation state, source data, camera, focus, or solar-mass behavior

PR24 grid warp controls:
- `W`: toggle mass-based grid warp visualization on/off
- grid warp affects only background grid rendering
- stronger mass creates stronger local warp; farther points warp less
- this is a visual metaphor only (not GR, geodesic solving, or lensing)
- grid warp does not alter body motion, forces, source data, trails, camera, focus, substeps, or solar-mass semantics

PR25 mass-aware warp constraints:
- grid warp strength now follows relative mass hierarchy (Sun dominates, Jupiter/Saturn weaker, terrestrial planets suppressed in overview)
- low-mass planets no longer appear Sun-like in far/overview views
- Sun runtime gravity multiplier still increases Sun warp via effective runtime mass mapping
- non-Sun warp does not get stronger just because Sun multiplier is increased

PR26 zoom-aware local warp behavior:
- keeps PR25 overview suppression for terrestrial planets
- when zoomed in, low-mass planets can show a small local warp
- local warp radius and displacement are capped in screen-space-derived bounds
- remains visual-only and does not alter physics/simulation/source data

PR27 smooth field behavior:
- smoothstep-based falloff softens line bending boundaries
- zoom fade reduces abrupt local warp popping near threshold
- soft-core distance avoids harsh center pulls
- top-K source limiting reduces awkward multi-body compounded kinks
- overview hierarchy and control mappings remain unchanged

PR28 spawn workflow shell behavior:
- right-clicking background opens a scrollable spawn menu
- clicking a template closes the menu and opens a read-only settings panel shell
- panel shows default values (mass/radius/velocity/color) plus derived volume/density
- `Set` and `Cancel` are visible; `Cancel` closes/discards draft
- `Set` only shows a pending note for future preview/spawn work
- no placement preview and no body spawn occur in PR28
- Black Hole entry is a placeholder template only, not a physical black hole simulation

Keyboard time controls:
- `Space`: pause/resume simulation stepping
- `[`: decrease time scale
- `]`: increase time scale
- `Ctrl+0`: reset time scale to `x1.0`

Review workflow:

`spec -> task -> agent -> harness -> review -> commit or rollback`
