# PR19 Acceptance Criteria

`PR19` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- camera view presets exist: `normal`, `overview`, `close`
- `B` cycles camera presets deterministically: `normal -> overview -> close -> normal`
- `0` resets camera to the current preset defaults
- camera view overlay status is visible and deterministic
- camera zoom step is configurable per camera state
- camera preset controls do not mutate physics state
- selection/inspector/time/fullscreen/mode/scale/solar-mass controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no physics substeps are added
- solar mass multiplier and absorption behavior are unchanged
- source data in `solar_system_data.py` is unchanged
- no mass-based grid distortion is added
- no GR/geodesic claim is made
- tests verify camera view logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
