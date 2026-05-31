import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.time_controls import (
    DEFAULT_MAX_TIME_SCALE,
    DEFAULT_MIN_TIME_SCALE,
    TimeControlState,
    compute_simulation_dt,
    decrease_time_scale,
    increase_time_scale,
    reset_time_scale,
    toggle_pause,
)


class TimeControlsTests(unittest.TestCase):
    def test_default_time_control_state_is_valid(self) -> None:
        state = TimeControlState()
        self.assertFalse(state.paused)
        self.assertAlmostEqual(state.time_scale, 1.0)
        self.assertGreater(state.min_time_scale, 0.0)
        self.assertGreater(state.max_time_scale, state.min_time_scale)
        self.assertGreater(state.dt_clamp_seconds, 0.0)

    def test_toggle_pause_changes_paused_state(self) -> None:
        state = TimeControlState(paused=False)
        paused = toggle_pause(state)
        resumed = toggle_pause(paused)
        self.assertTrue(paused.paused)
        self.assertFalse(resumed.paused)

    def test_paused_state_returns_zero_simulation_dt(self) -> None:
        state = TimeControlState(paused=True, time_scale=2.0)
        self.assertEqual(compute_simulation_dt(state, frame_dt_seconds=0.05), 0.0)

    def test_time_scale_increase_is_bounded_by_max(self) -> None:
        state = TimeControlState(time_scale=DEFAULT_MAX_TIME_SCALE)
        next_state = increase_time_scale(state, step=0.5)
        self.assertAlmostEqual(next_state.time_scale, DEFAULT_MAX_TIME_SCALE)

    def test_time_scale_decrease_is_bounded_by_min(self) -> None:
        state = TimeControlState(time_scale=DEFAULT_MIN_TIME_SCALE)
        next_state = decrease_time_scale(state, step=0.5)
        self.assertAlmostEqual(next_state.time_scale, DEFAULT_MIN_TIME_SCALE)

    def test_reset_time_scale_returns_to_one(self) -> None:
        state = TimeControlState(time_scale=2.7)
        next_state = reset_time_scale(state)
        self.assertAlmostEqual(next_state.time_scale, 1.0)

    def test_frame_dt_is_clamped_before_scaling(self) -> None:
        state = TimeControlState(time_scale=2.0, dt_clamp_seconds=0.1)
        simulation_dt = compute_simulation_dt(state, frame_dt_seconds=0.5)
        self.assertAlmostEqual(simulation_dt, 0.2)

    def test_controlled_dt_equals_clamped_dt_times_time_scale(self) -> None:
        state = TimeControlState(time_scale=1.5, dt_clamp_seconds=0.2)
        simulation_dt = compute_simulation_dt(state, frame_dt_seconds=0.12)
        self.assertAlmostEqual(simulation_dt, 0.18)

    def test_time_controls_do_not_mutate_physics_body_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        before_velocities = tuple(body.velocity_m_s for body in demo_state.physics_bodies)

        state = TimeControlState()
        _ = toggle_pause(state)
        _ = increase_time_scale(state)
        _ = decrease_time_scale(state)
        _ = reset_time_scale(state)
        _ = compute_simulation_dt(state, frame_dt_seconds=0.07)

        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
        self.assertEqual(before_velocities, tuple(body.velocity_m_s for body in demo_state.physics_bodies))
