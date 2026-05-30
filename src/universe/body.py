from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

Color = Tuple[int, int, int]
Point = Tuple[float, float]
BodyCategory = Literal["star", "terrestrial_planet", "gas_giant", "ice_giant"]


@dataclass(frozen=True)
class CelestialBody:
    name: str
    category: BodyCategory
    mass_kg: float
    mean_radius_m: float
    mean_orbital_radius_m: float
    orbital_period_s: float
    rotation_period_s: float
    color_rgb: Color
    visual_radius_px: float
    source_note: str


@dataclass(frozen=True)
class Body:
    data: CelestialBody
    world_x: float = 0.0
    world_y: float = 0.0

    @property
    def position(self) -> Point:
        return (self.world_x, self.world_y)

    @property
    def name(self) -> str:
        return self.data.name

    @property
    def draw_radius(self) -> float:
        return self.data.visual_radius_px

    @property
    def color(self) -> Color:
        return self.data.color_rgb
