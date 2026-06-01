# PR21 Acceptance Criteria

`PR21` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- default focus state is `Focus: none`
- selecting a body then pressing `F` sets focus to that body
- pressing `F` again on same selection clears focus
- focused body centers the camera while focus is active
- focus is cleared safely if focused body disappears
- dragging the camera clears focus
- selection/inspector/time/fullscreen/mode/scale/solar-mass/substeps/camera-view controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no adaptive timestep behavior is changed
- solar mass multiplier semantics remain unchanged
- source data in `solar_system_data.py` is unchanged
- no mass-based grid distortion is added
- no GR/geodesic claim is made
- tests verify focus-camera logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
