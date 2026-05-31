import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.display_modes import (
    DEFAULT_WINDOWED_SIZE,
    DisplayModeState,
    exit_fullscreen,
    toggle_fullscreen,
    update_windowed_size,
)


class DisplayModeTests(unittest.TestCase):
    def test_default_display_mode_is_windowed(self) -> None:
        state = DisplayModeState()
        self.assertFalse(state.is_fullscreen)
        self.assertEqual(state.windowed_size, DEFAULT_WINDOWED_SIZE)

    def test_toggling_from_windowed_enters_fullscreen(self) -> None:
        state = DisplayModeState(is_fullscreen=False, windowed_size=(1280, 720))
        next_state = toggle_fullscreen(state, current_size=(1400, 900))
        self.assertTrue(next_state.is_fullscreen)
        self.assertEqual(next_state.windowed_size, (1400, 900))

    def test_toggling_from_fullscreen_returns_to_windowed(self) -> None:
        state = DisplayModeState(is_fullscreen=True, windowed_size=(1200, 800))
        next_state = toggle_fullscreen(state, current_size=(1920, 1080))
        self.assertFalse(next_state.is_fullscreen)
        self.assertEqual(next_state.windowed_size, (1200, 800))

    def test_escape_exits_fullscreen(self) -> None:
        state = DisplayModeState(is_fullscreen=True, windowed_size=(1024, 768))
        next_state = exit_fullscreen(state, current_size=(1920, 1080))
        self.assertFalse(next_state.is_fullscreen)
        self.assertEqual(next_state.windowed_size, (1024, 768))

    def test_escape_in_windowed_mode_keeps_windowed_state(self) -> None:
        state = DisplayModeState(is_fullscreen=False, windowed_size=(1100, 700))
        next_state = exit_fullscreen(state, current_size=(1100, 700))
        self.assertEqual(next_state, state)

    def test_windowed_size_is_preserved_when_toggling(self) -> None:
        state = DisplayModeState(is_fullscreen=False, windowed_size=(1280, 720))
        fullscreen = toggle_fullscreen(state, current_size=(1333, 777))
        windowed = toggle_fullscreen(fullscreen, current_size=(1920, 1080))
        self.assertEqual(windowed.windowed_size, (1333, 777))

    def test_windowed_resize_updates_size_only_in_windowed_mode(self) -> None:
        windowed = DisplayModeState(is_fullscreen=False, windowed_size=(1280, 720))
        resized = update_windowed_size(windowed, windowed_size=(1500, 840))
        self.assertEqual(resized.windowed_size, (1500, 840))

        fullscreen = DisplayModeState(is_fullscreen=True, windowed_size=(1280, 720))
        unchanged = update_windowed_size(fullscreen, windowed_size=(1500, 840))
        self.assertEqual(unchanged.windowed_size, (1280, 720))

    def test_display_mode_state_changes_do_not_mutate_physics_body_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        before_velocities = tuple(body.velocity_m_s for body in demo_state.physics_bodies)

        state = DisplayModeState()
        state = toggle_fullscreen(state, current_size=(1280, 720))
        state = exit_fullscreen(state, current_size=(1920, 1080))
        _ = update_windowed_size(state, windowed_size=(1440, 900))

        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
        self.assertEqual(before_velocities, tuple(body.velocity_m_s for body in demo_state.physics_bodies))
