# Risk Register

| Risk | Mitigation |
| --- | --- |
| Demo simulation may be mistaken for real solar-system stability. | Keep controlled-demo wording explicit in docs and inspector warning text. |
| UI behavior may become overly complex while adding inspector interactions. | Keep PR8 inspector read-only and avoid adding editable controls or frameworks. |
| Input priority regressions may break drag behavior. | Preserve explicit priority: overlay controls > body selection > camera drag. |
| Selection hit testing might be inconsistent if tied to physical radius. | Use render-space hit testing with rendered radius and test deterministic selection logic. |
| Tests may accidentally require a display. | Keep selection and inspector formatting logic in pure helpers tested without opening a window. |
| Rollback may delete files if too aggressive. | Keep `rollback.sh` informational only and require human review before destructive commands. |
