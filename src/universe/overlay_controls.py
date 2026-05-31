from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

Point = Tuple[float, float]
Size = Tuple[int, int]
Rect = Tuple[int, int, int, int]

OVERLAY_LEFT = 16
OVERLAY_TOP = 16
OVERLAY_MIN_WIDTH = 180
OVERLAY_MAX_WIDTH = 260
OVERLAY_HEIGHT = 192
CONTROL_LEFT_PADDING = 16
CONTROL_WIDTH_PADDING = 32
LABELS_ROW_TOP = 18
TRAILS_ROW_TOP = 46
TIME_STATUS_ROW_TOP = 74
MODE_SCALE_STATUS_ROW_TOP = 102
EXPERIMENT_STATUS_ROW_TOP = 130
CAMERA_VIEW_STATUS_ROW_TOP = 158
CONTROL_ROW_HEIGHT = 22
CHECKBOX_CHECKED_TEXT = "[X]"
CHECKBOX_UNCHECKED_TEXT = "[ ]"


@dataclass(frozen=True)
class OverlayControlsState:
    show_labels: bool = True
    show_trails: bool = True


@dataclass(frozen=True)
class OverlayControlRects:
    panel_rect: Rect
    labels_rect: Rect
    trails_rect: Rect
    time_status_rect: Rect
    mode_scale_status_rect: Rect
    experiment_status_rect: Rect
    camera_view_status_rect: Rect


def overlay_panel_rect(viewport_size: Size) -> Rect:
    width = min(OVERLAY_MAX_WIDTH, viewport_size[0] - 32)
    width = max(width, OVERLAY_MIN_WIDTH)
    return (OVERLAY_LEFT, OVERLAY_TOP, width, OVERLAY_HEIGHT)


def build_overlay_control_rects(viewport_size: Size) -> OverlayControlRects:
    left, top, width, height = overlay_panel_rect(viewport_size)
    _ = height
    control_width = width - CONTROL_WIDTH_PADDING
    control_left = left + CONTROL_LEFT_PADDING
    return OverlayControlRects(
        panel_rect=(left, top, width, OVERLAY_HEIGHT),
        labels_rect=(control_left, top + LABELS_ROW_TOP, control_width, CONTROL_ROW_HEIGHT),
        trails_rect=(control_left, top + TRAILS_ROW_TOP, control_width, CONTROL_ROW_HEIGHT),
        time_status_rect=(
            control_left,
            top + TIME_STATUS_ROW_TOP,
            control_width,
            CONTROL_ROW_HEIGHT,
        ),
        mode_scale_status_rect=(
            control_left,
            top + MODE_SCALE_STATUS_ROW_TOP,
            control_width,
            CONTROL_ROW_HEIGHT,
        ),
        experiment_status_rect=(
            control_left,
            top + EXPERIMENT_STATUS_ROW_TOP,
            control_width,
            CONTROL_ROW_HEIGHT,
        ),
        camera_view_status_rect=(
            control_left,
            top + CAMERA_VIEW_STATUS_ROW_TOP,
            control_width,
            CONTROL_ROW_HEIGHT,
        ),
    )


def is_point_in_rect(point: Point, rect: Rect) -> bool:
    x, y = point
    left, top, width, height = rect
    return left <= x <= (left + width) and top <= y <= (top + height)


def handle_overlay_click(
    state: OverlayControlsState, point: Point, viewport_size: Size
) -> Tuple[OverlayControlsState, bool]:
    rects = build_overlay_control_rects(viewport_size)
    if is_point_in_rect(point, rects.labels_rect):
        return (OverlayControlsState(show_labels=not state.show_labels, show_trails=state.show_trails), True)
    if is_point_in_rect(point, rects.trails_rect):
        return (OverlayControlsState(show_labels=state.show_labels, show_trails=not state.show_trails), True)
    return (state, False)


def is_point_in_overlay_panel(point: Point, viewport_size: Size) -> bool:
    return is_point_in_rect(point, overlay_panel_rect(viewport_size))


def checkbox_label_text(label: str, enabled: bool) -> str:
    marker = CHECKBOX_CHECKED_TEXT if enabled else CHECKBOX_UNCHECKED_TEXT
    return f"{marker} {label}"
