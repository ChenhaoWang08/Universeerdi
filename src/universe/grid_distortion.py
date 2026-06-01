from __future__ import annotations

from dataclasses import dataclass, replace
from math import log10, sqrt
from typing import Mapping, Sequence, Tuple

from .body import Body

Point = Tuple[float, float]

DISTORTION_CENTER_EPSILON = 1e-12


@dataclass(frozen=True)
class GridDistortionState:
    enabled: bool = False
    strength: float = 1.0


@dataclass(frozen=True)
class DistortionSource:
    name: str
    position: Point
    mass_kg: float


def toggle_grid_distortion(state: GridDistortionState) -> GridDistortionState:
    return replace(state, enabled=not state.enabled)


def grid_distortion_status_text(state: GridDistortionState) -> str:
    if not state.enabled:
        return "Grid warp: off"
    return f"Grid warp: on x{state.strength:.1f}"


def distort_grid_point(
    point: Point,
    sources: Sequence[DistortionSource],
    *,
    strength: float,
    influence_radius_world: float,
    max_displacement_world: float,
) -> Point:
    _validate_distortion_parameters(
        strength=strength,
        influence_radius_world=influence_radius_world,
        max_displacement_world=max_displacement_world,
    )
    if not sources or strength == 0.0 or max_displacement_world == 0.0:
        return point

    point_x, point_y = point
    displacement_x = 0.0
    displacement_y = 0.0
    for source in sources:
        source_x, source_y = source.position
        delta_x = point_x - source_x
        delta_y = point_y - source_y
        distance = sqrt((delta_x * delta_x) + (delta_y * delta_y))
        if distance <= DISTORTION_CENTER_EPSILON:
            continue
        if distance >= influence_radius_world:
            continue

        unit_x = delta_x / distance
        unit_y = delta_y / distance
        falloff = (1.0 - (distance / influence_radius_world)) ** 2
        mass_scale = log10(max(source.mass_kg, 1.0)) / 30.0
        amount = falloff * mass_scale * strength * max_displacement_world
        displacement_x -= unit_x * amount
        displacement_y -= unit_y * amount

    total_displacement = sqrt((displacement_x * displacement_x) + (displacement_y * displacement_y))
    if total_displacement > max_displacement_world and total_displacement > 0.0:
        clamp = max_displacement_world / total_displacement
        displacement_x *= clamp
        displacement_y *= clamp

    return (point_x + displacement_x, point_y + displacement_y)


def build_distortion_sources_from_bodies(
    bodies: Sequence[Body],
    *,
    effective_masses_by_name: Mapping[str, float] | None = None,
) -> Tuple[DistortionSource, ...]:
    sources = []
    for body in bodies:
        base_mass = body.data.mass_kg
        effective_mass = (
            effective_masses_by_name.get(body.name, base_mass)
            if effective_masses_by_name is not None
            else base_mass
        )
        if effective_mass <= 0.0:
            continue
        sources.append(
            DistortionSource(
                name=body.name,
                position=body.position,
                mass_kg=effective_mass,
            )
        )
    return tuple(sources)


def _validate_distortion_parameters(
    *,
    strength: float,
    influence_radius_world: float,
    max_displacement_world: float,
) -> None:
    if strength < 0.0:
        raise ValueError("strength must be non-negative")
    if influence_radius_world <= 0.0:
        raise ValueError("influence_radius_world must be positive")
    if max_displacement_world < 0.0:
        raise ValueError("max_displacement_world must be non-negative")
