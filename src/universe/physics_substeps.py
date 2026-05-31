from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

SUBSTEP_VALUES: Tuple[int, ...] = (1, 2, 4, 8, 16)


@dataclass(frozen=True)
class PhysicsSubstepState:
    index: int = 0

    @property
    def substeps(self) -> int:
        return SUBSTEP_VALUES[self.index]


def increase_physics_substeps(state: PhysicsSubstepState) -> PhysicsSubstepState:
    return replace(state, index=min(state.index + 1, len(SUBSTEP_VALUES) - 1))


def decrease_physics_substeps(state: PhysicsSubstepState) -> PhysicsSubstepState:
    return replace(state, index=max(state.index - 1, 0))


def physics_substeps_status_text(state: PhysicsSubstepState) -> str:
    return f"Substeps: {state.substeps}"
