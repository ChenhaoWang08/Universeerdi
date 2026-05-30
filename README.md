# universeerdi

`universeerdi` is a Python + Pygame 2D top-down solar-system physics simulator project.

The long-term goal is an interactive viewer and simulation that can support camera pan and zoom, source-backed solar-system data, Newtonian N-body motion, and later visual or relativistic effects.

The current workflow is Spec-first Agent Engineering plus Agentic Harness Engineering.
`PR1` initialized control files and review workflow.
`PR2` implemented the minimal viewer foundation.
The current phase is `PR3`, which adds a real solar-system body data model and fixes PR2 stabilization issues without adding real physics yet.

Primary launch command:

```bash
python3 -m src.main
```

Alternative:

```bash
python -m src.main
```

Use the alternative only when `python` resolves to Python 3 on the local machine.

Real solar-system constants in `PR3` are based on official NASA and JPL references, while viewer layout positions remain placeholder display values.

Review workflow:

`spec -> task -> agent -> harness -> review -> commit or rollback`
