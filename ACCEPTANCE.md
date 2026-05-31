# PR12 Acceptance Criteria

`PR12` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- inspector supports controlled_demo bodies
- inspector supports solar_system bodies
- solar-system inspector shows name/mode/mass/position/velocity/speed/source
- radius is shown when available
- missing optional fields do not crash and do not invent data
- inspector remains read-only
- selection compatibility is preserved
- render scale policy remains compatible
- overlay/time controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no physical mass/position/velocity/radius is modified
- no ephemeris/JPL/network runtime integration is added
- no long-term stability claim is made
- tests verify inspector logic without opening a window
- existing physics/demo/overlay/selection tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
