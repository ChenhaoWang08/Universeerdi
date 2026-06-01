from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Tuple

TRAIL_LENGTH_VALUES: Tuple[int, ...] = (30, 60, 120, 240, 480)
TrailHistory = Dict[str, Tuple[Tuple[float, float], ...]]


@dataclass(frozen=True)
class TrailControlState:
    length_index: int = 2

    @property
    def max_points(self) -> int:
        return TRAIL_LENGTH_VALUES[self.length_index]


def increase_trail_length(state: TrailControlState) -> TrailControlState:
    return replace(state, length_index=min(state.length_index + 1, len(TRAIL_LENGTH_VALUES) - 1))


def decrease_trail_length(state: TrailControlState) -> TrailControlState:
    return replace(state, length_index=max(state.length_index - 1, 0))


def trail_length_status_text(state: TrailControlState) -> str:
    return f"Trail length: {state.max_points}"


def clear_trail_history() -> TrailHistory:
    return {}
