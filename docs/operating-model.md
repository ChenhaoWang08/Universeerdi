# Operating Model

- the human owns spec, acceptance, risk, review, and rollback decisions
- Codex implements only the current task scope
- source-backed constants should be documented when real data is introduced
- the harness records scenarios and judging rules
- scripts provide check and diff evidence
- commit only after review
- rollback is human-invoked after inspecting the diff
