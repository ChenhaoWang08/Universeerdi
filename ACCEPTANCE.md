# PR16 Acceptance Criteria

`PR16` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- Lorentz helper exists with speed-of-light constant
- `speed = 0` yields gamma `1.0`
- ordinary solar-system speeds yield gamma very close to `1.0`
- higher sub-light speeds yield larger gamma
- `speed >= c` behavior is safe and tested
- negative speed behavior is explicit and tested
- inspector displays `Lorentz gamma` for selected bodies
- Lorentz gamma is read-only display data
- Lorentz gamma does not mutate physics/simulation state
- Newtonian equations are unchanged
- no new integrator is added
- no physical mass/position/velocity/radius is modified
- no general relativity, geodesic, or spacetime-curvature claim is made
- no mass-based grid distortion is added
- tests verify Lorentz helpers without opening a window
- existing display/time/trails/selection/inspector tests still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
