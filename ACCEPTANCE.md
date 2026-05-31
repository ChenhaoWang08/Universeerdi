# PR17 Acceptance Criteria

`PR17` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- app starts in `controlled_demo` mode by default
- pressing `M` toggles to `solar_system` mode
- pressing `M` again toggles back to `controlled_demo`
- mode switch resets selection state safely
- mode switch clears trail history safely
- render-scale preset state includes `readable`, `realistic`, and `overview`
- pressing `V` cycles `readable -> realistic -> overview -> readable`
- selected preset can be injected into `solar_system_to_render_bodies(...)`
- render-scale presets affect rendering only
- overlay remains compact and includes mode + scale status text
- Labels/Trails checkbox controls remain compatible
- time controls remain compatible
- fullscreen/windowed controls remain compatible
- selection inspector remains compatible
- Newtonian equations are unchanged
- no new integrator is added
- no source dataset values are mutated
- no solar mass multiplier or absorption experiment is added
- tests verify mode/preset logic without opening a window
- existing physics/demo/solar_system/render_scale/time/display/selection/inspector/trails/overlay tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
