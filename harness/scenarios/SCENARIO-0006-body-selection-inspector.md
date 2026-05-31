# SCENARIO-0006: Demo Body Selection Inspector

## Goal

Verify that demo body selection and inspector behavior work as read-only rendering/runtime interactions.

## Steps

1. Launch the viewer.
2. Confirm overlay controls are visible and still clickable.
3. Click a demo body.
4. Confirm the selected body is visually highlighted.
5. Confirm inspector panel displays selected body fields.
6. Click empty background and confirm selection clears.
7. Confirm camera drag still works on background.
8. Confirm scroll-wheel zoom still works.

## Expected Result

- body selection and highlight work for demo bodies
- inspector panel shows read-only name/mass/position/velocity details
- selection does not edit bodies or change simulation correctness
- overlay controls remain prioritized over drag
- camera drag and zoom remain functional
