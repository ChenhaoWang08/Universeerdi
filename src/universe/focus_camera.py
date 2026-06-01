from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from .body import Body


@dataclass(frozen=True)
class FocusCameraState:
    focused_body_name: Optional[str] = None


def toggle_focus_from_selection(
    state: FocusCameraState,
    selected_body_name: Optional[str],
) -> FocusCameraState:
    if selected_body_name is None:
        return FocusCameraState()
    if state.focused_body_name == selected_body_name:
        return FocusCameraState()
    return FocusCameraState(focused_body_name=selected_body_name)


def clear_focus(state: FocusCameraState) -> FocusCameraState:
    _ = state
    return FocusCameraState()


def sync_focus_with_render_bodies(
    state: FocusCameraState,
    render_bodies: Sequence[Body],
) -> FocusCameraState:
    if state.focused_body_name is None:
        return state
    for body in render_bodies:
        if body.name == state.focused_body_name:
            return state
    return FocusCameraState()


def apply_focus_to_camera(
    camera: object,
    state: FocusCameraState,
    render_bodies: Sequence[Body],
) -> bool:
    if state.focused_body_name is None:
        return False
    for body in render_bodies:
        if body.name == state.focused_body_name:
            camera.center_x = body.world_x
            camera.center_y = body.world_y
            return True
    return False


def focus_status_text(state: FocusCameraState) -> str:
    if state.focused_body_name is None:
        return "Focus: none"
    return f"Focus: {state.focused_body_name}"
