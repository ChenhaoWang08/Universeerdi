# Risk Register

| Risk | Mitigation |
| --- | --- |
| Codex may overbuild real physics too early. | Keep `PR2` scope narrow in `SPEC.md`, `agent/task.md`, and review checklist. Reject real physics or real data in `PR2`. |
| The Pygame loop may become tangled. | Separate app loop, input, camera, grid, body data, and rendering responsibilities from the start. |
| Tests may accidentally require a display. | Keep camera and grid tests pure and non-windowed. Avoid display initialization in unit tests. |
| Zoom and grid logic may create too many lines. | Use zoom-aware grid spacing and cap visible density. Add non-window tests for spacing logic in `PR2`. |
| Real scale may make planets effectively invisible. | Keep physical scale separate from visual scale and allow visible-radius logic later. |
| Physical data may get mixed with placeholder display layout. | Keep SI fields in the solar-system dataset and keep viewer positions in the simulation layer. Add tests that verify the fields are separate. |
| Official source pages may be unavailable or drift over time. | Record active NASA and JPL source URLs, note rounding, and explicitly document fallback use when the NSSDCA fact-sheet site is unavailable. |
| UI may become too complex too early. | Limit `PR2` to a placeholder top-left UI area only. Delay real UI behavior to later phases. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
