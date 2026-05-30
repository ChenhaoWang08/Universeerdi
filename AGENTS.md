AGENTS.md

Repository Role

This repository is universeerdi.

universeerdi is a Python + Pygame project for building a 2D top-down solar-system physics simulator.

The project uses a combined workflow:

* Spec-first Agent Engineering: define goal, scope, non-goals, acceptance, risks, and rollback before implementation.
* Agentic Harness Engineering: verify agent work through tests, scripts, scenarios, judges, reports, and human review.

The agent must treat the human as the Spec Owner, Review Owner, Acceptance Owner, and Risk Owner.

⸻

Required Reading Before Any Change

Before making changes, read these files in order:

1. SPEC.md
2. ACCEPTANCE.md
3. RISKS.md
4. ROADMAP.md
5. agent/task.md
6. agent/policy.md
7. agent/allowed-files.md
8. agent/forbidden-files.md
9. agent/final-report-template.md

If the task touches physics, data, rendering, input, or simulation, also read:

* docs/architecture.md
* docs/data-sources.md
* src/universe/body.py
* src/universe/physics.py
* src/universe/simulation.py
* src/universe/solar_system_data.py
* src/universe/units.py

⸻

Core Working Rules

The agent must follow these rules:

1. Keep diffs small and reviewable.
2. Do not expand scope beyond the active task in agent/task.md.
3. Do not modify files listed in agent/forbidden-files.md.
4. Do not modify files outside agent/allowed-files.md unless the final report clearly explains why.
5. Do not add secrets, tokens, credentials, .env files, or private account data.
6. Do not auto-commit.
7. Do not push to GitHub.
8. Do not add deployment, networking, or external API behavior unless explicitly requested.
9. Do not add large frameworks or new dependencies unless the task explicitly allows it.
10. Run verification commands before the final response.
11. Write the final response using agent/final-report-template.md.

⸻

Current Project Direction

The final project goal is a 2D top-down solar-system simulator with:

* draggable camera
* mouse-wheel zoom
* dynamic background grid
* real solar-system body data
* Newtonian N-body physics
* future planet labels
* future orbit/trail display
* future Lorentz factor display
* future mass-based grid distortion visual effect

However, future goals must not be implemented early.

The agent must only implement the current PR task.

⸻

Physics Rules

Physics work must be handled carefully.

When implementing physics:

1. Use SI units internally.
2. Keep physical coordinates separate from screen coordinates.
3. Keep physical radius separate from visual render radius.
4. Do not hardcode circular orbits.
5. Do not fake stable solar-system behavior.
6. Do not claim real solar-system accuracy unless the task explicitly verifies it.
7. Do not introduce JPL Horizons, ephemeris, or astronomy libraries unless explicitly requested.
8. Keep physics logic pure and testable without Pygame.

For Newtonian gravity tasks:

* Implement pairwise gravitational acceleration.
* Sum acceleration from multiple bodies.
* Use explicit timestep-based updates.
* Document the integration method.
* Test zero-distance safety.
* Test self-interaction exclusion.

⸻

Rendering and Pygame Rules

Pygame code must stay separated from pure logic.

Rendering and UI work must follow these rules:

1. Pygame window logic belongs in the runtime layer.
2. Camera math must remain testable without opening a window.
3. Grid logic must remain testable without opening a window.
4. Physics tests must not require Pygame.
5. Automated tests must not open a GUI window.
6. Manual GUI verification must be reported separately.

For viewer behavior:

* Use python3 -m src.main as the primary launch command.
* Mention python -m src.main only as an alternative when python resolves to Python 3.
* Mouse-wheel zoom should have one authoritative event path.
* Do not reintroduce duplicate wheel-zoom handling.

⸻

Git and Baseline Rules

Before starting a new PR task, inspect git state:

git status --short
git log --oneline -5
git remote -v
git branch --show-current

Rules:

1. If the task requires a clean baseline and the working tree is not clean, stop and report.
2. Do not commit unless the human explicitly asks.
3. Do not push unless the human explicitly asks.
4. Do not rewrite git history.
5. Do not run destructive cleanup commands without human approval.
6. Use scripts/inspect-diff.sh to produce review evidence.

⸻

Verification Requirements

Before the final response, run the appropriate checks.

Default verification:

bash -n scripts/check.sh scripts/test.sh scripts/inspect-diff.sh scripts/rollback.sh
./scripts/test.sh
./scripts/check.sh
./scripts/inspect-diff.sh
python3 -m pytest tests

If the task changes viewer/runtime behavior, also document manual verification for:

python3 -m src.main

Manual GUI checks may include:

* window opens
* close button exits cleanly
* camera drag works
* mouse-wheel zoom works
* no traceback on normal close

Do not claim manual GUI behavior passed unless it was actually verified.

⸻

Safety Rules

The agent must not add or modify:

* .env
* .env.*
* secrets/
* credentials
* tokens
* API keys
* deployment files
* .github/workflows/
* binary assets
* generated cache files
* network-fetching code
* automatic commit scripts
* automatic push scripts

The agent must not call external APIs at runtime.

The agent must not fetch solar-system data from the network during program execution.

⸻

Dependency Rules

Current expected dependencies are minimal.

Allowed only when relevant:

* pygame
* pytest

Do not add new runtime dependencies unless the task explicitly requires them.

Do not add astronomy libraries, physics engines, UI frameworks, or network libraries unless explicitly approved.

If a dependency file is changed, explain:

1. what dependency was added
2. why it is needed
3. whether it is runtime or test-only
4. how to install it

⸻

Documentation Rules

When behavior changes, update the relevant docs.

Common files:

* README.md
* SPEC.md
* ACCEPTANCE.md
* RISKS.md
* CHANGELOG.md
* ROADMAP.md
* docs/architecture.md
* docs/data-sources.md
* agent/task.md

Do not over-edit unrelated documentation.

⸻

Harness and Review Rules

When a task changes acceptance behavior, update or check:

* harness/scenarios/
* harness/judges/
* reviews/

The agent must preserve the review path:

SPEC -> TASK -> IMPLEMENTATION -> TESTS -> HARNESS -> REVIEW -> HUMAN DECISION

The final decision belongs to the human.

⸻

Final Response

The final response must use agent/final-report-template.md.

At minimum, include:

1. Summary
2. Files changed
3. Commands run
4. Test results
5. Manual verification notes, if applicable
6. Acceptance check
7. Risks
8. Unresolved issues
9. Suggested next PR

Do not say work is complete unless verification evidence is provided.

Do not hide failed commands.

Do not summarize away important risks.

