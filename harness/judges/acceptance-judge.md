# Acceptance Judge

Judge `PR9` against `ACCEPTANCE.md`.

Pass only if:

- `solar_system` mode exists and `controlled_demo` still works
- solar-system states are built from existing dataset values
- Sun origin and planet initialization policy are deterministic and documented
- runtime stepping uses the existing Newtonian foundation (`step_bodies`)
- no per-frame circular animation path was introduced
- source dataset values are not mutated by builder logic
- no ephemeris/JPL/network runtime integration was introduced
- no physics equation changes were introduced
- all listed acceptance checks pass
