# universeerdi

`universeerdi` is a Python + Pygame 2D top-down solar-system physics simulator project.

The long-term goal is an interactive viewer and simulation that can support camera pan and zoom, source-backed solar-system data, Newtonian N-body motion, and later visual or relativistic effects.

The current workflow is Spec-first Agent Engineering plus Agentic Harness Engineering.
`PR1` initialized control files and review workflow.
`PR2` implemented the minimal viewer foundation.
`PR3` added the real solar-system body data foundation.
`PR4` added a pure Newtonian N-body physics foundation.
`PR5` connected controlled demo motion to physics stepping.
`PR6` added optional visual trails and labels.
`PR7` added clickable in-window overlay toggles.
`PR8` added a read-only demo body selection inspector.
The current phase is `PR9`, which adds a `solar_system` simulation mode using existing dataset values.

Primary launch command:

```bash
python3 -m src.main
```

Alternative:

```bash
python -m src.main
```

Use the alternative only when `python` resolves to Python 3 on the local machine.

Simulation modes are currently selected by `DEFAULT_SIMULATION_MODE` in [src/main.py](/Users/zhangyixin/Desktop/universeerdi/src/main.py):
- `"controlled_demo"`
- `"solar_system"`

PR9 `solar_system` mode uses deterministic initialization from existing data plus Newtonian stepping.
It does not claim high-precision ephemeris positions or long-term orbital stability guarantees.

Review workflow:

`spec -> task -> agent -> harness -> review -> commit or rollback`
