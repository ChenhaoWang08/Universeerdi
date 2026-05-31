# PR14 Acceptance Criteria

`PR14` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- app starts in windowed resizable mode
- F11 enters fullscreen
- F11 exits fullscreen
- Escape exits fullscreen
- windowed mode remains usable after fullscreen exit
- display mode state changes do not mutate physics/simulation state
- labels remain compatible
- selection/inspector remain compatible
- render scale policy remains compatible
- overlay/time controls remain compatible
- Newtonian equations are unchanged
- no new integrator is added
- no physical mass/position/velocity/radius is modified
- no save/load or complex display manager is added
- no ephemeris/JPL/network runtime integration is added
- no long-term stability claim is made
- tests verify display mode logic without opening a window
- existing physics/demo/overlay/selection tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
