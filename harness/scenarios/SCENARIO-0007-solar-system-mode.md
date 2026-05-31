# SCENARIO-0007: Solar-System Simulation Mode

## Goal

Verify that `solar_system` mode can run through the existing Newtonian stepping foundation using real dataset values.

## Steps

1. Set simulation mode to `solar_system`.
2. Launch the viewer.
3. Confirm no immediate traceback and normal frame updates.
4. Confirm bodies are rendered through the shared rendering path.
5. Confirm mode uses normal stepping flow (no direct circular animation playback).

## Expected Result

- `solar_system` mode initializes and runs
- stepping uses existing Newtonian physics pipeline
- no ephemeris fetch/integration path is required
- behavior is documented as deterministic initialization, not precision ephemeris stability
