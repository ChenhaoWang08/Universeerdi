# Risk Register

| Risk | Mitigation |
| --- | --- |
| Solar-system mode could be mistaken for precision ephemeris output. | Keep PR9 initialization policy documented and explicitly state non-ephemeris, non-stability guarantees. |
| Large SI distances may reduce viewer readability. | Use explicit physical-to-render mapping with deterministic position/radius conversion rules. |
| Dashed trail geometry could render inconsistently across segment lengths. | Keep dash-splitting math pure, deterministic, and covered by non-window tests. |
| Trail color handling could break for malformed color data. | Resolve colors through a safe fallback path before rendering. |
| Hidden-trail sessions could accumulate unbounded history. | Keep trail history updates bounded regardless of visibility toggle. |
| Selection/inspector behavior may regress while touching render path. | Preserve existing pipelines and run compatibility tests with full suite. |
| Tests may accidentally require a display. | Keep solar-system builder and stepping tests pure and non-windowed. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
