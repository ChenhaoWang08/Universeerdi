# Risk Register

| Risk | Mitigation |
| --- | --- |
| Solar-system mode could be mistaken for precision ephemeris output. | Keep PR9 initialization policy documented and explicitly state non-ephemeris, non-stability guarantees. |
| Large SI distances may reduce viewer readability. | Use explicit physical-to-render mapping with deterministic position/radius conversion rules. |
| Fullscreen mode switches may desynchronize internal size assumptions. | Centralize display-mode state and always derive rendering/input behavior from current surface size. |
| Escape behavior could regress windowed quit flow. | Keep conditional logic explicit: escape fullscreen first, otherwise preserve existing quit behavior. |
| Windowed size may be lost after fullscreen toggle. | Track and restore last known windowed size in a pure display-mode state model. |
| Selection/inspector behavior may regress while touching render path. | Preserve existing pipelines and run compatibility tests with full suite. |
| Tests may accidentally require a display. | Keep solar-system builder and stepping tests pure and non-windowed. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
