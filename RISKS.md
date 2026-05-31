# Risk Register

| Risk | Mitigation |
| --- | --- |
| Solar-system mode could be mistaken for precision ephemeris output. | Document PR9 initialization policy and explicitly state non-ephemeris, non-stability guarantees. |
| Large SI distances may reduce viewer readability. | Keep physics in SI and use rendering scale conversion only for display compatibility. |
| Input/render behavior may regress while adding a new mode. | Keep existing mode paths and run full non-window and runtime smoke checks. |
| Approximate initial velocity policy may be misunderstood as per-frame circular animation. | Use circular-speed estimate for initialization only and step runtime through `step_bodies(...)`. |
| Tests may accidentally require a display. | Keep solar-system builder and stepping tests pure and non-windowed. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
