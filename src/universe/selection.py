from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Optional, Sequence, Tuple

from .body import Body
from .physics import PhysicsBodyState

Point = Tuple[float, float]
Size = Tuple[int, int]


@dataclass(frozen=True)
class SelectionState:
    selected_body_name: Optional[str] = None


def select_body_at_screen_point(
    bodies: Sequence[Body],
    camera: object,
    point: Point,
    viewport_size: Size,
) -> Optional[str]:
    """Return body name at point; if overlap exists, closest center wins."""
    point_x, point_y = point
    closest_distance = None
    closest_name = None

    for body in bodies:
        body_x, body_y = camera.world_to_screen(body.position, viewport_size)
        radius = max(6.0, body.draw_radius * camera.zoom)
        delta_x = point_x - body_x
        delta_y = point_y - body_y
        distance_squared = (delta_x * delta_x) + (delta_y * delta_y)
        if distance_squared > (radius * radius):
            continue
        if closest_distance is None or distance_squared < closest_distance:
            closest_distance = distance_squared
            closest_name = body.name

    return closest_name


def handle_body_selection_click(
    state: SelectionState,
    bodies: Sequence[Body],
    camera: object,
    point: Point,
    viewport_size: Size,
) -> Tuple[SelectionState, bool]:
    selected_name = select_body_at_screen_point(bodies, camera, point, viewport_size)
    if selected_name is None:
        # Empty background click clears selection and is not consumed.
        return (SelectionState(), False)

    if state.selected_body_name == selected_name:
        return (state, True)
    return (SelectionState(selected_body_name=selected_name), True)


def get_selected_physics_body(
    bodies: Sequence[PhysicsBodyState], selected_body_name: Optional[str]
) -> Optional[PhysicsBodyState]:
    if selected_body_name is None:
        return None
    for body in bodies:
        if body.name == selected_body_name:
            return body
    return None


def format_body_inspector_lines(body: Optional[PhysicsBodyState]) -> Tuple[str, ...]:
    if body is None:
        return (
            "Selected Body",
            "Name: None",
            "Click a demo body to inspect.",
        )

    speed = sqrt((body.velocity_m_s.x**2) + (body.velocity_m_s.y**2))
    return (
        "Selected Body",
        f"Name: {body.name}",
        f"Mass: {body.mass_kg:.3e} kg",
        f"Position: x={body.position_m.x:.3f} m, y={body.position_m.y:.3f} m",
        f"Velocity: vx={body.velocity_m_s.x:.3f} m/s, vy={body.velocity_m_s.y:.3f} m/s",
        f"Speed: {speed:.3f} m/s",
        "Demo-only inspector (not real solar-system validation).",
    )
