# PR22 Acceptance Criteria

`PR22` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- distance scale ruler helper exists and is deterministic
- distance labels support meters, km, and AU
- ruler distance uses camera zoom and meters_per_world_unit
- ruler is shown in `solar_system` mode
- controlled demo does not show solar-system distance ruler
- render-scale explanations exist for readable/realistic/overview
- ruler/explanation are informational only
- selection/inspector/time/fullscreen/mode/scale/solar-mass/substeps/camera-view/focus controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no adaptive timestep behavior is changed
- solar mass multiplier semantics remain unchanged
- source data in `solar_system_data.py` is unchanged
- no mass-based grid distortion is added
- no GR/geodesic claim is made
- tests verify scale-ruler logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
