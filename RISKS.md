# Risk Register

| Risk | Mitigation |
| --- | --- |
| Demo simulation may be mistaken for real solar-system stability. | Keep controlled-demo wording explicit in docs and source notes. |
| Overlay controls may grow into unscoped UI complexity. | Keep PR7 controls as simple in-window toggles with no UI framework. |
| Trails may hurt readability or performance if unbounded. | Keep per-body trail history bounded and test helper behavior. |
| Input handling may regress camera drag behavior. | Prioritize UI clicks before drag start and keep drag checks covered by helper tests. |
| Tests may accidentally require a display. | Keep control logic and hitbox behavior in pure helpers tested without opening a window. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
