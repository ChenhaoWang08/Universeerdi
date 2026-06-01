# Scenario 0018: Editable Spawn Settings Fields

## Goal

Verify PR29 settings-panel editing + validation while preserving no-preview/no-spawn behavior.

## Steps

1. Launch `python3 -m src.main`.
2. Right-click empty background and open spawn menu.
3. Select a template and open settings panel.
4. Edit Name/Mass/Radius/Velocity/Color fields.
5. Press `Set` with valid values and confirm valid note appears.
6. Enter invalid values (for example mass empty, RGB out of range) and press `Set`.
7. Confirm validation errors are shown and panel stays open.
8. Confirm no placement preview and no body spawn happen.
9. Click `Cancel` and confirm panel closes/discards draft.

## Expected

- Editable fields support cursor-based single-line editing.
- Validation feedback is deterministic.
- No physics/runtime spawn side effects are introduced.
