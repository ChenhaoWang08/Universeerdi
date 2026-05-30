# Risk Register

| Risk | Mitigation |
| --- | --- |
| Demo simulation may be mistaken for real solar-system stability. | Keep controlled-demo wording explicit in docs and source notes. |
| Overlay rendering may grow into unscoped UI complexity. | Keep PR6 controls as simple runtime feature flags, not UI controls. |
| Trails may hurt readability or performance if unbounded. | Cap per-body trail history with a fixed max length and test helper behavior. |
| The Pygame loop may become tangled. | Keep trail-history updates in pure helpers and leave loop changes minimal. |
| Tests may accidentally require a display. | Keep trail/label logic tests non-windowed and avoid display initialization. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
