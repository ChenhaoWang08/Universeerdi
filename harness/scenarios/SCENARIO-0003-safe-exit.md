# SCENARIO-0003: Safe Exit

## Goal

Verify that closing the viewer exits safely.

## Steps

1. Launch the app with `python3 -m src.main`.
2. Close the window using the window close control.
3. Observe terminal behavior after exit.

## Expected Result

- the close event exits cleanly
- no traceback is printed
- no hanging process remains
