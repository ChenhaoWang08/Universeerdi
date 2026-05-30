# SCENARIO-0002: Controlled Demo Physics Motion

## Goal

Verify that `PR5` uses a controlled demo simulation stepped by PR4 Newtonian physics, without claiming real solar-system stability.

## Steps

1. Launch the viewer.
2. Confirm that demo bodies move over time.
3. Confirm that motion is demo-only and not presented as real solar-system stability.
4. Confirm that camera drag and zoom remain available.

## Expected Result

- controlled demo bodies are visible and moving
- movement comes from physics stepping, not hardcoded circular animation
- real solar-system dataset remains separate from demo motion
- viewer controls remain functional
