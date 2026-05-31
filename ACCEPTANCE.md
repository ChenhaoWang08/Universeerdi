# PR20 Acceptance Criteria

`PR20` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- default physics substeps is `1`
- `=` increases physics substeps
- `-` decreases physics substeps
- overlay shows deterministic `Substeps: N` status
- solar-system stepping accepts `physics_substeps`
- `physics_substeps=1` preserves prior behavior
- absorption is applied after each substep
- invalid `physics_substeps` values are explicitly rejected
- selection/inspector/time/fullscreen/mode/scale/solar-mass/camera-view controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no adaptive timestep is added
- solar mass multiplier semantics remain unchanged
- source data in `solar_system_data.py` is unchanged
- no mass-based grid distortion is added
- no GR/geodesic claim is made
- tests verify substep logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
