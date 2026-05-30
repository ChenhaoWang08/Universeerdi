# SCENARIO-0001: Window Launch

## Goal

Verify that the `PR3` viewer foundation launches correctly.

## Steps

1. Run `python3 -m src.main`.
2. Confirm that a resizable non-fullscreen window opens.
3. Confirm that a dark gray background is visible.
4. Close the window.

## Expected Result

- the app launches without immediate failure
- the window is resizable
- the background is visible
- the process exits cleanly

## Manual Check Command

`python3 -m src.main`
