# PR9 Acceptance Criteria

`PR9` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `solar_system` mode exists
- `controlled_demo` mode still works
- solar-system body states are built from existing dataset values
- Sun starts at or near origin
- planets start with nonzero meter-scale positions
- planet velocities are finite
- runtime motion comes from `step_bodies(...)`
- no hardcoded per-frame circular orbit animation is introduced
- source dataset is not mutated
- Newtonian equations are unchanged
- no ephemeris/JPL/network runtime integration is added
- no long-term stability claim is made
- tests verify solar-system mode without opening a window
- existing physics/demo/overlay/selection tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
