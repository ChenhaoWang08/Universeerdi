# PR25 Acceptance Criteria

`PR25` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- grid distortion default state is off
- `W` toggles grid distortion on/off
- overlay displays deterministic grid warp status text
- grid warp uses relative-to-Sun mass scaling hierarchy
- Sun visual warp factor is greater than Jupiter, and Jupiter greater than Earth
- terrestrial planets are suppressed or near-invisible in overview warp
- influence radius scales with visual mass factor
- grid distortion affects only grid rendering and is bounded
- larger mass causes stronger or equal distortion at equal distance
- farther points cause weaker or equal distortion for equal source mass
- point-at-source-center path is safe (no divide-by-zero crash)
- Sun multiplier increases Sun visual warp only; non-Sun masses do not inflate from Sun multiplier
- PR23 trail controls remain unchanged (`C`, `,`, `.` + status)
- selection/inspector/time/fullscreen/mode/scale/solar-mass/substeps/camera-view/focus controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- solar mass multiplier semantics remain unchanged
- absorption behavior remains unchanged
- source data in `solar_system_data.py` is unchanged
- no GR/geodesic/lensing claim is made
- tests verify grid-distortion logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
