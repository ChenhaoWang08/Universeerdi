# TASK-0001: Create Project Foundation

## Objective

Initialize the workflow control files for `universeerdi` so future implementation work is safe, reviewable, testable, and rollbackable.

## Allowed Files

- `README.md`
- `AGENTS.md`
- `SPEC.md`
- `ACCEPTANCE.md`
- `RISKS.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `specs/active/SPEC-0001-pygame-universe-foundation.md`
- `tasks/todo/TASK-0001-create-project-foundation.md`
- `agent/`
- `harness/scenarios/`
- `harness/judges/`
- `reviews/REVIEW-0001-pygame-universe-foundation.md`
- `docs/architecture.md`
- `docs/operating-model.md`
- `docs/decisions/ADR-0001-use-pygame-for-2d-universe.md`
- `scripts/check.sh`
- `scripts/inspect-diff.sh`
- `scripts/rollback.sh`

## Forbidden Files and Actions

- do not implement Pygame code
- do not modify `src/` implementation files
- do not modify `tests/` implementation files
- do not install `pygame`
- do not install `pytest`
- do not add secrets, `.env` files, binary files, networking, or deployment config
- do not auto-commit

## Verification

- review the filled workflow documents for scope alignment
- run `scripts/check.sh`
- run `scripts/inspect-diff.sh`

## Acceptance

- the repository contains clear spec, acceptance, risk, task, harness, review, and rollback guidance for `PR2`
- no Pygame implementation code is added in `PR1`
- rollback remains human-controlled

## Next Task

`PR2: Create Pygame solar-system viewer foundation`
