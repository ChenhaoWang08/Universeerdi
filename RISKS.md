# Risk Register

| Risk | Mitigation |
| --- | --- |
| Solar-system mode could be mistaken for precision ephemeris output. | Keep PR9 initialization policy documented and explicitly state non-ephemeris, non-stability guarantees. |
| Large SI distances may reduce viewer readability. | Keep physics in SI and use rendering scale conversion only for display compatibility. |
| Input/render behavior may regress while adding time-control keys. | Keep controls minimal, preserve drag/zoom paths, and run full non-window plus runtime smoke checks. |
| Time-scale increases can destabilize stepping if frame dt spikes. | Clamp frame dt before scaling and bound time-scale range. |
| Pause behavior might accidentally freeze rendering. | Keep render loop running and only gate simulation stepping dt. |
| Tests may accidentally require a display. | Keep solar-system builder and stepping tests pure and non-windowed. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
