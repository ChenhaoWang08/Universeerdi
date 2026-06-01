# Risk Register

| Risk | Mitigation |
| --- | --- |
| Solar-system mode could be mistaken for precision ephemeris output. | Keep PR9 initialization policy documented and explicitly state non-ephemeris, non-stability guarantees. |
| Large SI distances may reduce viewer readability. | Use explicit physical-to-render mapping with deterministic position/radius conversion rules. |
| Fullscreen mode switches may desynchronize internal size assumptions. | Centralize display-mode state and always derive rendering/input behavior from current surface size. |
| Checkbox-style overlay refactor could break click hitbox routing. | Keep hitbox math in `overlay_controls.py` and verify click-consumed behavior with non-window tests. |
| Checkbox/status row layout could become unreadable at runtime. | Keep overlay rows deterministic and compact; preserve dedicated status row and run manual viewer smoke check. |
| Lorentz gamma display could be misread as full relativity simulation. | Document clearly that gamma is read-only display metric and is not fed into Newtonian stepping. |
| Invalid speed input policy could be ambiguous near or above light speed. | Keep explicit helper behavior: `speed < 0` raises, `speed >= c` returns `inf`, and cover with tests. |
| Runtime mode switching could leave stale selection/trail state. | Reset selection and trail history when mode toggles, and verify with deterministic tests. |
| Render-scale presets might be misread as physics changes. | Keep preset logic in rendering policy layer only and assert no mutation of physics state/dataset. |
| Solar mass multiplier could be mistaken for source-data mutation. | Keep multiplier runtime-only in stepping path and restore baseline Sun mass in stored state. |
| Simple absorption may be mistaken for physically realistic collision modeling. | Document absorption as an experimental visualization rule, not fluid dynamics or GR model. |
| Camera view presets could accidentally reset non-camera runtime state. | Restrict preset application to camera fields only and verify mode/time/experiment compatibility with tests and viewer smoke check. |
| Large frame dt under high gravity can skip over absorption checks. | Split solar-system frame dt into fixed substeps and apply absorption after each slice with deterministic tests. |
| Focused target may disappear while camera follow is active. | Reconcile focus against current render bodies each frame and clear focus when missing. |
| Scale presets may be misinterpreted as physics mode changes. | Show ruler + concise preset notes as informational UI while preserving unchanged physics/state behavior. |
| Trail history can become visually noisy after mode/experiment shifts. | Add direct clear control and bounded runtime trail length controls with deterministic trimming. |
| Mass-based grid warp could be misread as true GR/geodesic physics. | Label the feature as visual-only and keep distortion logic isolated to grid rendering with no force coupling. |
| Relative mass hierarchy in grid warp could be visually misleading at overview zoom. | Use reference-mass scaling + visibility threshold + influence-radius constraints so Sun remains dominant. |
| Close-up views may hide small-body warp completely after overview suppression. | Add zoom-aware local warp path with strict screen-space caps to show local effects without polluting overview. |
| Escape behavior could regress windowed quit flow. | Keep conditional logic explicit: escape fullscreen first, otherwise preserve existing quit behavior. |
| Windowed size may be lost after fullscreen toggle. | Track and restore last known windowed size in a pure display-mode state model. |
| Selection/inspector behavior may regress while touching render path. | Preserve existing pipelines and run compatibility tests with full suite. |
| Tests may accidentally require a display. | Keep solar-system builder and stepping tests pure and non-windowed. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
