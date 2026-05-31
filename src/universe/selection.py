from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from .body import Body
from .inspector import SimulationMode, build_inspector_lines
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
        radius = max(1.0, body.draw_radius * camera.zoom)
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


def format_body_inspector_lines(
    body: Optional[PhysicsBodyState],
    *,
    simulation_mode: SimulationMode = "controlled_demo",
) -> Tuple[str, ...]:
    return build_inspector_lines(
        body,
        simulation_mode=simulation_mode,
    )
