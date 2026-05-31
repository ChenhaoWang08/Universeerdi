from __future__ import annotations

from math import sqrt
from typing import Literal, Optional, Tuple

from .body import CelestialBody
from .demo_simulation import DEMO_BODY_DATA_BY_NAME
from .physics import PhysicsBodyState
from .solar_system_data import SOLAR_SYSTEM_BODY_MAP

SimulationMode = Literal["placeholder", "controlled_demo", "solar_system"]

SOLAR_SYSTEM_SOURCE_LABEL = "local solar_system_data.py dataset (no live API)"
DEMO_SOURCE_LABEL = "demo-only (no live API)"
UNKNOWN_SOURCE_LABEL = "unknown"


def build_inspector_lines(
    selected_physics_body: Optional[PhysicsBodyState],
    *,
    simulation_mode: SimulationMode,
) -> Tuple[str, ...]:
    if selected_physics_body is None:
        return (
            "Selected Body",
            "Name: None",
            "Click a body to inspect.",
        )

    metadata, source_label = _resolve_body_metadata(
        selected_physics_body.name,
        simulation_mode,
    )
    speed_m_s = _speed(selected_physics_body)
    distance_m = _distance_from_origin(selected_physics_body)

    radius_text = _radius_text(metadata, simulation_mode)
    lines = [
        "Selected Body",
        f"Name: {selected_physics_body.name}",
        f"Mode: {simulation_mode}",
        f"Mass: {_fmt_sci(selected_physics_body.mass_kg)} kg",
        f"Radius: {radius_text}",
        (
            "Position: "
            f"x={_fmt_sci(selected_physics_body.position_m.x)} m, "
            f"y={_fmt_sci(selected_physics_body.position_m.y)} m"
        ),
        (
            "Velocity: "
            f"vx={_fmt_sci(selected_physics_body.velocity_m_s.x)} m/s, "
            f"vy={_fmt_sci(selected_physics_body.velocity_m_s.y)} m/s"
        ),
        f"Speed: {_fmt_sci(speed_m_s)} m/s",
        f"Distance: {_fmt_sci(distance_m)} m",
    ]

    if simulation_mode == "solar_system":
        lines.extend(_solar_system_optional_lines(metadata))

    lines.append(f"Source: {source_label}")
    return tuple(lines)


def _resolve_body_metadata(
    body_name: str,
    simulation_mode: SimulationMode,
) -> Tuple[Optional[CelestialBody], str]:
    if simulation_mode == "solar_system":
        body_data = SOLAR_SYSTEM_BODY_MAP.get(body_name)
        return (body_data, SOLAR_SYSTEM_SOURCE_LABEL if body_data is not None else UNKNOWN_SOURCE_LABEL)
    if simulation_mode == "controlled_demo":
        body_data = DEMO_BODY_DATA_BY_NAME.get(body_name)
        return (body_data, DEMO_SOURCE_LABEL if body_data is not None else UNKNOWN_SOURCE_LABEL)
    return (None, UNKNOWN_SOURCE_LABEL)


def _radius_text(body_data: Optional[CelestialBody], simulation_mode: SimulationMode) -> str:
    if simulation_mode != "solar_system":
        return "unknown"
    if body_data is None:
        return "unknown"
    if body_data.mean_radius_m <= 0.0:
        return "unknown"
    return f"{_fmt_sci(body_data.mean_radius_m)} m"


def _solar_system_optional_lines(body_data: Optional[CelestialBody]) -> Tuple[str, ...]:
    if body_data is None:
        return (
            "Mean Orbit Radius: unknown",
            "Orbital Period: unknown",
            "Rotation Period: unknown",
        )

    return (
        f"Mean Orbit Radius: {_fmt_sci(body_data.mean_orbital_radius_m)} m",
        (
            "Orbital Period: "
            f"{_fmt_sci(body_data.orbital_period_s)} s "
            f"({_fmt_sci(_seconds_to_days(body_data.orbital_period_s))} days)"
        ),
        (
            "Rotation Period: "
            f"{_fmt_sci(body_data.rotation_period_s)} s "
            f"({_fmt_sci(_seconds_to_days(body_data.rotation_period_s))} days)"
        ),
    )


def _speed(body: PhysicsBodyState) -> float:
    return sqrt((body.velocity_m_s.x**2) + (body.velocity_m_s.y**2))


def _distance_from_origin(body: PhysicsBodyState) -> float:
    return sqrt((body.position_m.x**2) + (body.position_m.y**2))


def _seconds_to_days(seconds: float) -> float:
    return seconds / 86_400.0


def _fmt_sci(value: float) -> str:
    return f"{value:.3e}"
