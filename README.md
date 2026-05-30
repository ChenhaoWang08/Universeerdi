# universeerdi

`universeerdi` is a Python + Pygame 2D top-down solar-system physics simulator project.

The long-term goal is an interactive viewer and simulation that can support camera pan and zoom, source-backed solar-system data, Newtonian N-body motion, and later visual or relativistic effects.

The current workflow is Spec-first Agent Engineering plus Agentic Harness Engineering.
`PR1` initialized control files and review workflow.
`PR2` implemented the minimal viewer foundation.
`PR3` added the real solar-system body data foundation.
`PR4` added a pure Newtonian N-body physics foundation.
The current phase is `PR5`, which connects that physics foundation to a controlled demo simulation without claiming real solar-system stability.

Primary launch command:

```bash
python3 -m src.main
```

Alternative:

```bash
python -m src.main
```

Use the alternative only when `python` resolves to Python 3 on the local machine.

Real solar-system constants are still kept separate from the PR5 controlled demo bodies.
PR5 demo motion is for physics verification and visualization only.

Review workflow:

`spec -> task -> agent -> harness -> review -> commit or rollback`
