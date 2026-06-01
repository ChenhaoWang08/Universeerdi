import unittest

from src.universe.trails import (
    DEFAULT_TRAIL_FALLBACK_COLOR,
    build_dashed_polyline_segments,
    resolve_trail_color,
    split_line_into_dashed_segments,
    trim_trail_history,
    update_trail_history_bounded,
)


class TrailsTests(unittest.TestCase):
    def test_dashed_helper_returns_no_segments_for_empty_or_single_point_input(self) -> None:
        self.assertEqual(build_dashed_polyline_segments(()), ())
        self.assertEqual(build_dashed_polyline_segments(((1.0, 1.0),)), ())

    def test_dashed_helper_returns_deterministic_segments_for_horizontal_line(self) -> None:
        segments = split_line_into_dashed_segments(
            (0.0, 0.0),
            (25.0, 0.0),
            dash_length=10.0,
            gap_length=5.0,
        )
        self.assertEqual(
            segments,
            (
                ((0.0, 0.0), (10.0, 0.0)),
                ((15.0, 0.0), (25.0, 0.0)),
            ),
        )

    def test_dashed_helper_handles_diagonal_lines(self) -> None:
        segments = split_line_into_dashed_segments(
            (0.0, 0.0),
            (30.0, 30.0),
            dash_length=8.0,
            gap_length=4.0,
        )
        self.assertGreaterEqual(len(segments), 2)
        self.assertEqual(segments[0][0], (0.0, 0.0))
        self.assertLessEqual(segments[-1][1][0], 30.0)
        self.assertLessEqual(segments[-1][1][1], 30.0)

    def test_trail_history_is_bounded_to_max_length(self) -> None:
        history = {}
        history = update_trail_history_bounded(history, {"Earth": (0.0, 0.0)}, max_points=3)
        history = update_trail_history_bounded(history, {"Earth": (1.0, 0.0)}, max_points=3)
        history = update_trail_history_bounded(history, {"Earth": (2.0, 0.0)}, max_points=3)
        history = update_trail_history_bounded(history, {"Earth": (3.0, 0.0)}, max_points=3)
        self.assertEqual(history["Earth"], ((1.0, 0.0), (2.0, 0.0), (3.0, 0.0)))

    def test_body_colored_trail_selection_uses_body_color_when_available(self) -> None:
        self.assertEqual(resolve_trail_color((120, 45, 200)), (120, 45, 200))

    def test_fallback_trail_color_is_safe_when_body_color_missing(self) -> None:
        self.assertEqual(resolve_trail_color(None), DEFAULT_TRAIL_FALLBACK_COLOR)
        self.assertEqual(resolve_trail_color((1, 2)), DEFAULT_TRAIL_FALLBACK_COLOR)

    def test_show_trails_false_is_rendering_only_and_history_can_still_be_bounded(self) -> None:
        hidden_history = {}
        for index in range(10):
            hidden_history = update_trail_history_bounded(
                hidden_history,
                {"Mars": (float(index), 0.0)},
                max_points=4,
            )
        self.assertEqual(len(hidden_history["Mars"]), 4)

    def test_trail_helpers_do_not_mutate_input_point_history(self) -> None:
        points = ((0.0, 0.0), (10.0, 0.0), (20.0, 0.0))
        points_before = tuple(points)
        _segments = build_dashed_polyline_segments(points, dash_length=5.0, gap_length=2.0)
        self.assertEqual(points, points_before)

    def test_trim_trail_history_rejects_invalid_max_points(self) -> None:
        with self.assertRaises(ValueError):
            trim_trail_history({}, 0)

    def test_trim_trail_history_keeps_most_recent_points(self) -> None:
        history = {
            "Earth": ((0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)),
        }
        trimmed = trim_trail_history(history, 2)
        self.assertEqual(trimmed["Earth"], ((2.0, 0.0), (3.0, 0.0)))

    def test_trim_trail_history_preserves_body_names(self) -> None:
        history = {
            "Earth": ((0.0, 0.0),),
            "Mars": ((1.0, 1.0), (2.0, 2.0)),
        }
        trimmed = trim_trail_history(history, 1)
        self.assertEqual(set(trimmed.keys()), {"Earth", "Mars"})
