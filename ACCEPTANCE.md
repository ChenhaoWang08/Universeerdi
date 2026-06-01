# PR28 Acceptance Criteria

`PR28` is accepted only if all of the following are true:

- `python3 -m src.main` remains the documented primary launch command
- `controlled_demo` mode still works
- `solar_system` mode still works
- existing key mappings remain unchanged (`W`, `G/H/R`, `M`, `V`, `B`, `F`, `C`, `,`, `.`, `Space`, `F11`)
- right-clicking background opens the spawn menu
- right-clicking a body does not open the spawn menu
- right-clicking overlay/inspector does not open the spawn menu
- spawn menu is scrollable and clamped to viewport bounds
- spawn menu contains Sun + planets + Black Hole placeholder
- menu hover highlight is visible and deterministic
- clicking a template closes menu and opens settings panel shell
- clicking a template does not create placement preview
- clicking a template does not spawn a body
- settings panel fields are read-only in PR28
- panel shows derived `volume` and `density`
- panel has `Set` and `Cancel` buttons
- `Cancel` closes panel and discards draft
- `Set` does not create preview and does not spawn a body
- spawn workflow shell does not change physics state
- Newtonian equations are unchanged
- source data in `solar_system_data.py` is unchanged
- `camera_views.py` behavior is unchanged
- grid warp behavior is unchanged
- Black Hole is documented as placeholder only (not physical black hole simulation)
- tests for spawn workflow logic pass without opening a window
- existing test suites still pass
- `scripts/check.sh` passes
- `python3 -m pytest tests` passes
- no secrets, credentials, `.env`, binary assets, or deployment files are added
