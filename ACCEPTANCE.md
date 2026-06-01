# PR29 Acceptance Criteria

`PR29` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- PR28 spawn menu behavior remains intact
- clicking a template still opens settings panel (no preview/spawn)
- editable fields exist: Name, Mass kg, Radius m, Velocity X, Velocity Y, Color RGB
- clicking a field does not clear existing text
- cursor-based single-line editing works
- Backspace/Delete/Left/Right/Ctrl-A(or Cmd-A) editing behavior works
- text input while panel-focused does not trigger global hotkeys
- Set validates draft fields
- valid Set shows a valid draft note and keeps panel open
- invalid Set shows validation errors and keeps panel open
- Volume and Density are derived read-only values
- Cancel closes panel and discards draft edits
- no placement preview is created
- no body is spawned
- key mappings remain unchanged (`W`, `G/H/R`, `M`, `V`, `B`, `F`, `C`, `,`, `.`, `Space`, `F11`)
- Newtonian equations are unchanged
- source data in `solar_system_data.py` is unchanged
- `camera_views.py` behavior is unchanged
- grid warp behavior is unchanged
- Black Hole template remains placeholder only (not physical black hole simulation)
- tests for spawn workflow editing/validation pass without opening a window
- existing test suites still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
