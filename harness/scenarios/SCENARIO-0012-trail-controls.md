# SCENARIO-0012: Trail Controls

## Goal

Verify PR23 runtime trail reset and trail-length controls.

## Preconditions

- Launch with `python3 -m src.main`

## Steps

1. Enable trails and let history accumulate.
2. Press `C`; confirm trails clear immediately.
3. Press `.` repeatedly; confirm trail length status increases.
4. Press `,` repeatedly; confirm trail length status decreases.
5. While shrinking length, confirm existing long trails trim quickly.
6. Switch mode/preset and solar-mass/substep controls; confirm no traceback.

## Expected Result

- Trail history can be cleared without restart.
- Trail length can be adjusted safely at runtime.
- Trail controls only affect trail-history storage/rendering, not physics/simulation state.
