# Risk Register

| Risk | Mitigation |
| --- | --- |
| Solar-system mode could be mistaken for precision ephemeris output. | Keep PR9 initialization policy documented and explicitly state non-ephemeris, non-stability guarantees. |
| Large SI distances may reduce viewer readability. | Use explicit physical-to-render mapping with deterministic position/radius conversion rules. |
| Render-scale tuning could be mistaken for physics tuning. | Keep SI physics state immutable and document that mapping is display-only. |
| Selection/hit testing may drift if radius mapping changes. | Ensure selection uses rendered radius and add non-window compatibility tests. |
| Overlay/time-control behavior might regress while touching render path. | Keep integration minimal and run full non-window plus runtime smoke checks. |
| Tests may accidentally require a display. | Keep solar-system builder and stepping tests pure and non-windowed. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
