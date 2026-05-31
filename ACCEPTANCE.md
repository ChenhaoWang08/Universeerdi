# PR11 Acceptance Criteria

`PR11` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- render scale policy exists
- physical positions map to render positions without mutating physics state
- physical radii map to visible radii with minimum and maximum clamps
- selection uses rendered position/radius behavior
- inspector continues reporting physical values
- labels/trails/toggles/time overlay remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no physical mass/position/velocity/radius is modified for visual readability
- no ephemeris/JPL/network runtime integration is added
- no long-term stability claim is made
- tests verify render-scale logic without opening a window
- existing physics/demo/overlay/selection tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
