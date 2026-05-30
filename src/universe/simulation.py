from __future__ import annotations

from typing import Tuple

from .body import Body
from .solar_system_data import get_solar_system_body

DEFAULT_WINDOW_SIZE = (1280, 720)
MIN_WINDOW_SIZE = (800, 600)

PLACEHOLDER_LAYOUT = (
    ("Sun", (0.0, 0.0)),
    ("Mercury", (110.0, -140.0)),
    ("Venus", (200.0, 70.0)),
    ("Earth", (290.0, -100.0)),
    ("Mars", (400.0, 140.0)),
    ("Jupiter", (520.0, -160.0)),
    ("Saturn", (620.0, 20.0)),
    ("Uranus", (730.0, -110.0)),
    ("Neptune", (840.0, 150.0)),
)


def create_placeholder_bodies() -> Tuple[Body, ...]:
    return tuple(
        Body(
            data=get_solar_system_body(name),
            world_x=position[0],
            world_y=position[1],
        )
        for name, position in PLACEHOLDER_LAYOUT
    )
