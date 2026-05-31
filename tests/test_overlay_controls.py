import unittest

from src.universe.demo_simulation import create_controlled_demo_state
from src.universe.overlay_controls import (
    OverlayControlsState,
    build_overlay_control_rects,
    checkbox_label_text,
    handle_overlay_click,
)


class OverlayControlsTests(unittest.TestCase):
    def test_default_overlay_state_is_enabled_for_labels_and_trails(self) -> None:
        state = OverlayControlsState()
        self.assertTrue(state.show_labels)
        self.assertTrue(state.show_trails)

    def test_clicking_inside_labels_control_toggles_labels(self) -> None:
        state = OverlayControlsState(show_labels=True, show_trails=True)
        rects = build_overlay_control_rects((1280, 720))
        click_point = (rects.labels_rect[0] + 3, rects.labels_rect[1] + 3)
        next_state, consumed = handle_overlay_click(state, click_point, (1280, 720))
        self.assertTrue(consumed)
        self.assertFalse(next_state.show_labels)
        self.assertTrue(next_state.show_trails)

    def test_clicking_inside_trails_control_toggles_trails(self) -> None:
        state = OverlayControlsState(show_labels=True, show_trails=True)
        rects = build_overlay_control_rects((1280, 720))
        click_point = (rects.trails_rect[0] + 3, rects.trails_rect[1] + 3)
        next_state, consumed = handle_overlay_click(state, click_point, (1280, 720))
        self.assertTrue(consumed)
        self.assertTrue(next_state.show_labels)
        self.assertFalse(next_state.show_trails)

    def test_clicking_outside_controls_does_not_toggle(self) -> None:
        state = OverlayControlsState(show_labels=False, show_trails=True)
        next_state, consumed = handle_overlay_click(state, (700.0, 500.0), (1280, 720))
        self.assertFalse(consumed)
        self.assertEqual(next_state, state)

    def test_clicking_control_is_consumed(self) -> None:
        state = OverlayControlsState()
        rects = build_overlay_control_rects((1280, 720))
        click_point = (rects.labels_rect[0] + 1, rects.labels_rect[1] + 1)
        _, consumed = handle_overlay_click(state, click_point, (1280, 720))
        self.assertTrue(consumed)

    def test_control_rectangles_are_deterministic(self) -> None:
        first = build_overlay_control_rects((1280, 720))
        second = build_overlay_control_rects((1280, 720))
        self.assertEqual(first, second)

    def test_checkbox_label_text_reflects_checked_state(self) -> None:
        self.assertEqual(checkbox_label_text("Labels", True), "[X] Labels")

    def test_checkbox_label_text_reflects_unchecked_state(self) -> None:
        self.assertEqual(checkbox_label_text("Trails", False), "[ ] Trails")

    def test_time_status_row_is_positioned_below_checkbox_rows(self) -> None:
        rects = build_overlay_control_rects((1280, 720))
        labels_bottom = rects.labels_rect[1] + rects.labels_rect[3]
        trails_bottom = rects.trails_rect[1] + rects.trails_rect[3]
        time_top = rects.time_status_rect[1]
        panel_bottom = rects.panel_rect[1] + rects.panel_rect[3]
        self.assertGreater(time_top, labels_bottom)
        self.assertGreater(time_top, trails_bottom)
        self.assertLessEqual(time_top + rects.time_status_rect[3], panel_bottom)

    def test_mode_scale_status_row_is_positioned_below_time_status(self) -> None:
        rects = build_overlay_control_rects((1280, 720))
        time_bottom = rects.time_status_rect[1] + rects.time_status_rect[3]
        mode_scale_top = rects.mode_scale_status_rect[1]
        panel_bottom = rects.panel_rect[1] + rects.panel_rect[3]
        self.assertGreater(mode_scale_top, time_bottom)
        self.assertLessEqual(mode_scale_top + rects.mode_scale_status_rect[3], panel_bottom)

    def test_experiment_status_row_is_positioned_below_mode_scale(self) -> None:
        rects = build_overlay_control_rects((1280, 720))
        mode_scale_bottom = rects.mode_scale_status_rect[1] + rects.mode_scale_status_rect[3]
        experiment_top = rects.experiment_status_rect[1]
        panel_bottom = rects.panel_rect[1] + rects.panel_rect[3]
        self.assertGreater(experiment_top, mode_scale_bottom)
        self.assertLessEqual(experiment_top + rects.experiment_status_rect[3], panel_bottom)

    def test_toggle_clicks_do_not_mutate_physics_state(self) -> None:
        demo_state = create_controlled_demo_state()
        before_positions = tuple(body.position_m for body in demo_state.physics_bodies)
        before_velocities = tuple(body.velocity_m_s for body in demo_state.physics_bodies)

        rects = build_overlay_control_rects((1280, 720))
        _state, _consumed = handle_overlay_click(
            OverlayControlsState(),
            (rects.labels_rect[0] + 2, rects.labels_rect[1] + 2),
            (1280, 720),
        )

        self.assertEqual(before_positions, tuple(body.position_m for body in demo_state.physics_bodies))
        self.assertEqual(before_velocities, tuple(body.velocity_m_s for body in demo_state.physics_bodies))
