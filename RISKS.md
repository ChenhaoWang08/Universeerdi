# Risk Register

| Risk | Mitigation |
| --- | --- |
| Demo simulation may be mistaken for real solar-system stability. | Label PR5 demo bodies clearly as controlled verification-only data and keep real dataset separate. |
| Codex may overbuild real physics too early. | Keep scope narrow in `SPEC.md`, `agent/task.md`, and review checklist. |
| The Pygame loop may become tangled. | Keep demo stepping logic in pure simulation modules and keep runtime loop minimal. |
| Tests may accidentally require a display. | Keep demo and physics tests non-windowed and avoid display initialization in unit tests. |
| Zoom and grid logic may regress while integrating demo motion. | Preserve existing camera/grid tests and run full check scripts. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
