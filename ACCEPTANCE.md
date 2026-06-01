# PR23 Acceptance Criteria

`PR23` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- default trail length is `120`
- `C` clears trail history
- `.` increases trail length
- `,` decreases trail length
- decreasing trail length trims existing history immediately
- increasing trail length preserves existing history
- overlay displays current trail length deterministically
- trail rendering remains dashed and body-colored
- selection/inspector/time/fullscreen/mode/scale/solar-mass/substeps/camera-view/focus controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no adaptive timestep behavior is changed
- solar mass multiplier semantics remain unchanged
- source data in `solar_system_data.py` is unchanged
- no mass-based grid distortion is added
- no GR/geodesic claim is made
- tests verify trail-control logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
