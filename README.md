# universeerdi

`universeerdi` is a Python + Pygame 2D top-down solar-system physics simulator project.

The long-term goal is an interactive viewer and simulation that can support camera pan and zoom, source-backed solar-system data, Newtonian N-body motion, and later visual or relativistic effects.

The current workflow is Spec-first Agent Engineering plus Agentic Harness Engineering.
`PR1` initialized control files and review workflow.
`PR2` implemented the minimal viewer foundation.
`PR3` added the real solar-system body data foundation.
`PR4` added a pure Newtonian N-body physics foundation.
`PR5` connected controlled demo motion to physics stepping.
The current phase is `PR6`, which adds optional trails and labels behind feature flags for controlled demo rendering.

Primary launch command:

```bash
python3 -m src.main
```

Alternative:

```bash
python -m src.main
```

Use the alternative only when `python` resolves to Python 3 on the local machine.

Real solar-system constants remain separate from controlled demo bodies.
PR6 overlays are visual-only and do not alter physics calculations.

Review workflow:

`spec -> task -> agent -> harness -> review -> commit or rollback`
