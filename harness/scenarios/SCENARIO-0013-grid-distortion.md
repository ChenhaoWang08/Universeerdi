# SCENARIO-0013: Grid Distortion Visual Toggle

## Goal

Verify PR24 mass-based grid distortion remains visual-only and runtime-toggleable.

## Preconditions

- viewer launches with `python3 -m src.main`
- simulator starts in `controlled_demo` mode by default

## Steps

1. Press `W` once.
2. Confirm overlay shows `Grid warp: on x1.0`.
3. Observe that grid lines bend/compress near massive bodies.
4. Press `W` again.
5. Confirm overlay shows `Grid warp: off`.
6. Verify `G/H/R`, `C`, `,`, `.`, `M`, `V`, `B`, `0`, `F`, `Space`, `F11` still respond as before.

## Expected

- Grid distortion changes only grid rendering.
- Bodies, trails, and physics stepping semantics remain unchanged.
- No traceback occurs during toggling.
