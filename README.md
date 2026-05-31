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
`PR9` added a `solar_system` simulation mode using existing dataset values.
`PR10` added pause/resume, bounded time scale, and dt clamp controls for simulation stepping.
`PR11` added physical-to-render scale policy and visible radius clamps.
The current phase is `PR12`, which extends the read-only inspector for real solar-system fields.

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

PR10 time controls affect simulation stepping frequency only.
PR10 does not change Newtonian physics equations.

PR11 separates physical simulation units from rendering scale.
Physics continues using SI units; rendering applies visual mapping plus minimum/maximum visible radii.

PR12 inspector fields are display-only.
Solar-system inspector values come from local `solar_system_data.py` plus runtime physics state (no live API calls).

Keyboard time controls:
- `Space`: pause/resume simulation stepping
- `[` or `-`: decrease time scale
- `]` or `=`: increase time scale
- `0`: reset time scale to `x1.0`

Review workflow:

`spec -> task -> agent -> harness -> review -> commit or rollback`
