# PR13 Acceptance Criteria

`PR13` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- trails use body color or safe fallback
- trails render as dashed paths
- trail history is bounded
- empty/short trail histories are safe
- show_trails toggle remains compatible
- labels remain compatible
- selection/inspector remain compatible
- render scale policy remains compatible
- overlay/time controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no physical mass/position/velocity/radius is modified
- no orbit prediction or hardcoded circular animation is added
- no ephemeris/JPL/network runtime integration is added
- no long-term stability claim is made
- tests verify trail helpers without opening a window
- existing physics/demo/overlay/selection tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
