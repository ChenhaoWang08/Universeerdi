from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

SimulationMode = Literal["controlled_demo", "solar_system"]


@dataclass(frozen=True)
class SimulationModeState:
    mode: SimulationMode = "controlled_demo"


def toggle_simulation_mode(state: SimulationModeState) -> SimulationModeState:
    next_mode: SimulationMode = (
        "solar_system" if state.mode == "controlled_demo" else "controlled_demo"
    )
    return replace(state, mode=next_mode)


def simulation_mode_status_text(state: SimulationModeState) -> str:
    return f"Mode: {state.mode}"
