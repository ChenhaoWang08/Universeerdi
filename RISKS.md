# Risk Register

| Risk | Mitigation |
| --- | --- |
| Solar-system mode could be mistaken for precision ephemeris output. | Keep PR9 initialization policy documented and explicitly state non-ephemeris, non-stability guarantees. |
| Large SI distances may reduce viewer readability. | Use explicit physical-to-render mapping with deterministic position/radius conversion rules. |
| Inspector fields could be mistaken for live API data. | Label source as local `solar_system_data.py` and explicitly note no live API calls. |
| Inspector expansion could reduce readability. | Keep lines concise, use scientific notation for large SI values, and avoid dense prose blocks. |
| Selection/hit testing may regress while inspector logic evolves. | Keep selection name-based and run compatibility tests for selection + overlay interaction. |
| Overlay/time-control behavior might regress while touching inspector rendering path. | Keep integration minimal and run full non-window plus runtime smoke checks. |
| Tests may accidentally require a display. | Keep solar-system builder and stepping tests pure and non-windowed. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
