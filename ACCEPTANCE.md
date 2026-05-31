# PR10 Acceptance Criteria

`PR10` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- pause/resume state exists and is runtime-usable
- time scale exists with lower and upper bounds
- frame dt is clamped before simulation stepping
- paused mode prevents stepping (or applies zero simulation dt)
- overlay shows running/paused state and current scale
- keyboard controls for pause/resume and scale are documented
- runtime stepping still comes from existing simulation/physics path
- Newtonian equations are unchanged
- no new integrator is added
- no ephemeris/JPL/network runtime integration is added
- no long-term stability claim is made
- tests verify time-control logic without opening a window
- existing physics/demo/overlay/selection tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
