import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.trail_controls import (
    TRAIL_LENGTH_VALUES,
    TrailControlState,
    clear_trail_history,
    decrease_trail_length,
    increase_trail_length,
    trail_length_status_text,
)
from src.universe.trails import trim_trail_history, update_trail_history_bounded


class TrailControlsTests(unittest.TestCase):
    def test_default_trail_length_is_120(self) -> None:
        state = TrailControlState()
        self.assertEqual(state.max_points, 120)

    def test_increase_length_advances_to_next_value(self) -> None:
        state = TrailControlState()
        state = increase_trail_length(state)
        self.assertEqual(state.max_points, 240)

    def test_decrease_length_moves_to_previous_value(self) -> None:
        state = TrailControlState(length_index=2)
        state = decrease_trail_length(state)
        self.assertEqual(state.max_points, 60)

    def test_length_clamps_at_bounds(self) -> None:
        min_state = TrailControlState(length_index=0)
        max_state = TrailControlState(length_index=len(TRAIL_LENGTH_VALUES) - 1)
        self.assertEqual(decrease_trail_length(min_state).max_points, TRAIL_LENGTH_VALUES[0])
        self.assertEqual(increase_trail_length(max_state).max_points, TRAIL_LENGTH_VALUES[-1])

    def test_trail_status_text_is_deterministic(self) -> None:
        state = TrailControlState(length_index=2)
        self.assertEqual(trail_length_status_text(state), "Trail length: 120")

    def test_clear_trail_history_returns_empty_history(self) -> None:
        self.assertEqual(clear_trail_history(), {})

    def test_decreasing_length_trims_existing_history_immediately(self) -> None:
        history = {}
        for index in range(8):
            history = update_trail_history_bounded(
                history,
                {"Earth": (float(index), 0.0)},
                max_points=120,
            )
        state = TrailControlState(length_index=2)
        next_state = decrease_trail_length(state)  # 60
        trimmed = trim_trail_history(history, next_state.max_points)
        self.assertLessEqual(len(trimmed["Earth"]), next_state.max_points)

    def test_increasing_length_preserves_existing_history(self) -> None:
        history = {}
        for index in range(5):
            history = update_trail_history_bounded(
                history,
                {"Earth": (float(index), 0.0)},
                max_points=120,
            )
        state = TrailControlState(length_index=2)
        next_state = increase_trail_length(state)  # 240
        self.assertEqual(next_state.max_points, 240)
        self.assertEqual(history["Earth"], ((0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)))

    def test_helpers_do_not_mutate_physics_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        state = TrailControlState()
        _ = increase_trail_length(state)
        _ = decrease_trail_length(state)
        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
