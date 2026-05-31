# PR15 Acceptance Criteria

`PR15` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- overlay Labels control is rendered as checkbox-style text
- overlay Trails control is rendered as checkbox-style text
- checkbox checked/unchecked text matches `show_labels` and `show_trails` state
- labels hitbox still toggles label visibility
- trails hitbox still toggles trail visibility
- overlay control clicks are consumed
- overlay control clicks do not trigger body selection or camera drag
- time/display status text remains visible in the top-left overlay
- selection/inspector behavior remains compatible
- fullscreen/windowed behavior remains compatible
- time controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no physical mass/position/velocity/radius is modified
- no save/load or UI framework is added
- no ephemeris/JPL/network runtime integration is added
- no long-term stability claim is made
- tests verify checkbox/control logic without opening a window
- existing display/time/trails/selection/inspector tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
