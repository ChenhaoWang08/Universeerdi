from __future__ import annotations

from math import hypot
from typing import Dict, Sequence, Tuple

Point = Tuple[float, float]
LineSegment = Tuple[Point, Point]
TrailHistory = Dict[str, Tuple[Point, ...]]
Color = Tuple[int, int, int]

DEFAULT_TRAIL_FALLBACK_COLOR: Color = (180, 186, 198)
DEFAULT_DASH_LENGTH = 10.0
DEFAULT_GAP_LENGTH = 7.0


def build_dashed_polyline_segments(
    points: Sequence[Point],
    *,
    dash_length: float = DEFAULT_DASH_LENGTH,
    gap_length: float = DEFAULT_GAP_LENGTH,
) -> Tuple[LineSegment, ...]:
    if len(points) < 2:
        return ()
    _validate_dash_params(dash_length, gap_length)

    dashed_segments = []
    for start, end in zip(points, points[1:]):
        dashed_segments.extend(
            split_line_into_dashed_segments(
                start,
                end,
                dash_length=dash_length,
                gap_length=gap_length,
            )
        )
    return tuple(dashed_segments)


def split_line_into_dashed_segments(
    start: Point,
    end: Point,
    *,
    dash_length: float = DEFAULT_DASH_LENGTH,
    gap_length: float = DEFAULT_GAP_LENGTH,
) -> Tuple[LineSegment, ...]:
    _validate_dash_params(dash_length, gap_length)
    start_x, start_y = start
    end_x, end_y = end
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    line_length = hypot(delta_x, delta_y)
    if line_length <= 0.0:
        return ()

    unit_x = delta_x / line_length
    unit_y = delta_y / line_length
    stride = dash_length + gap_length
    segments = []
    progress = 0.0
    while progress < line_length:
        dash_start = progress
        dash_end = min(progress + dash_length, line_length)
        segment_start = (
            start_x + (unit_x * dash_start),
            start_y + (unit_y * dash_start),
        )
        segment_end = (
            start_x + (unit_x * dash_end),
            start_y + (unit_y * dash_end),
        )
        segments.append((segment_start, segment_end))
        progress += stride
    return tuple(segments)


def resolve_trail_color(
    body_color: Color | None,
    *,
    fallback_color: Color = DEFAULT_TRAIL_FALLBACK_COLOR,
) -> Color:
    if body_color is None or len(body_color) != 3:
        return fallback_color
    return tuple(
        max(0, min(255, int(channel)))
        for channel in body_color
    )


def update_trail_history_bounded(
    trail_history: TrailHistory,
    points_by_name: Dict[str, Point],
    *,
    max_points: int,
) -> TrailHistory:
    if max_points <= 0:
        raise ValueError("max_points must be positive")

    next_history: TrailHistory = {}
    for name, point in points_by_name.items():
        previous_points = trail_history.get(name, ())
        combined = previous_points + (point,)
        next_history[name] = combined[-max_points:]
    return next_history


def _validate_dash_params(dash_length: float, gap_length: float) -> None:
    if dash_length <= 0.0:
        raise ValueError("dash_length must be positive")
    if gap_length < 0.0:
        raise ValueError("gap_length must be non-negative")
