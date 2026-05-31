# PR18 Acceptance Criteria

`PR18` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- baseline source data in `solar_system_data.py` is unchanged
- runtime Sun gravity multiplier exists and is controllable at runtime
- runtime Sun gravity multiplier affects solar-system stepping behavior
- baseline initial orbital velocity logic remains tied to baseline Sun source mass
- non-Sun bodies inside Sun physical radius are absorbed safely
- absorption rule is deterministic and test-covered
- overlay status includes current Sun gravity experiment state
- selection/inspector/time/fullscreen/mode/preset controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no mass-based grid distortion is added
- no GR/geodesic claim is made
- tests verify multiplier and absorption logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
