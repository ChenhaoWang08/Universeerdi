from __future__ import annotations

from typing import Sequence, Tuple

from .body import Body


def step_placeholder_bodies(
    bodies: Sequence[Body], delta_seconds: float
) -> Tuple[Body, ...]:
    """PR3 intentionally preserves the no-physics placeholder contract."""
    _ = delta_seconds
    return tuple(bodies)
