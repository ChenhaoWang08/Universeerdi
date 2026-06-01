# SCENARIO-0010: Focus Body Camera

## Goal

Verify PR21 focus follow behavior for selected bodies.

## Preconditions

- Launch with `python3 -m src.main`
- Switch to `solar_system` mode with `M` if needed

## Steps

1. Confirm overlay shows `Focus: none` initially.
2. Click Earth to select it, then press `F`.
3. Confirm overlay shows `Focus: Earth`.
4. Confirm camera center follows Earth while simulation advances.
5. Press `F` again and confirm focus clears.
6. Re-enable focus, then drag camera manually; confirm focus clears.
7. Under high gravity settings, if a focused body is absorbed, confirm focus clears without traceback.

## Expected Result

- Focus state toggles deterministically with `F`.
- Camera follow tracks focused body while it exists.
- Missing focused body is cleared safely.
- Other controls remain compatible.
